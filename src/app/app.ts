import { NgClass } from '@angular/common';
import { ChangeDetectionStrategy, Component, ElementRef, OnDestroy, ViewChild, signal } from '@angular/core';
import { environment } from '../environments/environment';

interface DetectionStatus {
  message: string;
  safe: boolean;
  total: number;
  con_casco: number;
  sin_casco: number;
  unmatched_helmets?: number;
  warning?: string;
}

interface Statistics {
  totalDetections: number;
  safeDetections: number;
  unsafeDetections: number;
  lastDetectionTime: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [NgClass],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnDestroy {
  mode = signal<'selection' | 'upload' | 'realtime'>('selection');
  isLoading = signal(false);
  statistics = signal<Statistics>({
    totalDetections: 0,
    safeDetections: 0,
    unsafeDetections: 0,
    lastDetectionTime: ''
  });

  preview = signal<string | ArrayBuffer | null>(null);
  resultado = signal<string | null>(null);
  imagen = signal<File | null>(null);

  @ViewChild('videoEl') videoEl!: ElementRef<HTMLVideoElement>;
  @ViewChild('canvasEl') canvasEl!: ElementRef<HTMLCanvasElement>;
  private stream: MediaStream | null = null;
  private intervalId: number | null = null;
  private busy = false;

  private readonly detectUrl = `${environment.apiUrl}/detect/`;
  isCameraOn = signal(false);
  isDetecting = signal(false);
  status = signal<DetectionStatus | null>(null);
  annotatedImageUrl = signal<string | null>(null);

  selectMode(newMode: 'upload' | 'realtime' | 'selection') {
    if (newMode === 'selection' || newMode !== this.mode()) {
      this.stopRealtimeDetection();
      this.stopCamera();
      this.resultado.set(null);
      this.status.set(null);
      this.annotatedImageUrl.set(null);
      this.preview.set(null);
      this.imagen.set(null);
    }
    this.mode.set(newMode);
  }

  onFileSelected(event: any) {
    const file = event.target.files?.[0];
    if (!file) return;

    this.imagen.set(file);
    const reader = new FileReader();
    reader.onload = () => this.preview.set(reader.result);
    reader.readAsDataURL(file);

    this.resultado.set(null);
    this.status.set(null);
    this.annotatedImageUrl.set(null);
  }

  async procesar() {
    const currentImagen = this.imagen();
    if (!currentImagen) {
      this.resultado.set('⚠️ Selecciona una imagen primero.');
      return;
    }

    this.isLoading.set(true);
    this.resultado.set('⏳ Analizando imagen con IA...');
    this.status.set(null);
    this.annotatedImageUrl.set(null);

    try {
      const formData = new FormData();
      formData.append('file', currentImagen);

      const resJson = await fetch(this.detectUrl, { method: 'POST', body: formData });
      if (!resJson.ok) {
        const error = await resJson.text();
        console.error('Error del servidor:', error);
        this.resultado.set(`❌ Error: ${resJson.status} - ${resJson.statusText}`);
        this.isLoading.set(false);
        return;
      }

      const json = (await resJson.json()) as DetectionStatus;
      this.status.set(json);

      this.resultado.set(json.message);      // Actualizar estadísticas
      this.updateStatistics(json.safe);

      if (json.safe === false) {
        this.playAlertSound();
        await this.sendWhatsAppAlert("⚠️ ALERTA: Persona sin casco detectada.");
      }

      const formData2 = new FormData();
      formData2.append('file', currentImagen);
      const resImage = await fetch(`${environment.apiUrl}/detect/image`, { method: 'POST', body: formData2 });

      if (resImage.ok) {
        const blob = await resImage.blob();
        const prevUrl = this.annotatedImageUrl();
        if (prevUrl) URL.revokeObjectURL(prevUrl);
        this.annotatedImageUrl.set(URL.createObjectURL(blob));
      }
    } catch (error) {
      console.error('Error al enviar imagen:', error);
      this.resultado.set(`❌ Error de conexión. Verifica que la API esté activa.`);
    } finally {
      this.isLoading.set(false);
    }
  }

  private updateStatistics(isSafe: boolean) {
    const current = this.statistics();
    this.statistics.set({
      totalDetections: current.totalDetections + 1,
      safeDetections: isSafe ? current.safeDetections + 1 : current.safeDetections,
      unsafeDetections: !isSafe ? current.unsafeDetections + 1 : current.unsafeDetections,
      lastDetectionTime: new Date().toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    });
  }

  private playAlertSound() {
    try {
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();

      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);

      oscillator.frequency.value = 800;
      oscillator.type = 'sine';
      gainNode.gain.value = 0.3;

      oscillator.start(audioContext.currentTime);
      oscillator.stop(audioContext.currentTime + 0.2);

      setTimeout(() => {
        oscillator.frequency.value = 600;
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.2);
      }, 250);
    } catch (e) {
      console.warn('No se pudo reproducir sonido de alerta', e);
    }
  }

  resetStatistics() {
    this.statistics.set({
      totalDetections: 0,
      safeDetections: 0,
      unsafeDetections: 0,
      lastDetectionTime: ''
    });
  }

  async startCamera() {
    if (this.isCameraOn()) return;
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: false });
      const video = this.videoEl.nativeElement;
      video.srcObject = this.stream;
      await video.play();
      this.isCameraOn.set(true);
      this.resultado.set('📹 Cámara activada. Sistema listo para detección.');
      this.status.set(null);
      this.annotatedImageUrl.set(null);
    } catch (e) {
      console.error('No se pudo iniciar la cámara', e);
      this.isCameraOn.set(false);
      this.resultado.set('❌ Permiso de cámara denegado. Permite el acceso para continuar.');
    }
  }

  private async sendWhatsAppAlert(message: string): Promise<void> {
    try {
      const res = await fetch(`${environment.apiUrl}/alert/whatsapp`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });

      if (!res.ok) {
        console.error('Error al enviar alerta WhatsApp:', await res.text());
      }
    } catch (error) {
      console.error('Error al enviar alerta WhatsApp:', error);
    }
  }

  stopCamera() {
    this.stopRealtimeDetection();
    if (!this.stream) return;
    this.stream.getTracks().forEach(t => t.stop());
    this.stream = null;
    this.isCameraOn.set(false);
    this.resultado.set('Cámara apagada.');
  }

  startRealtimeDetection(intervalMs = 800) {
    if (!this.isCameraOn() || this.isDetecting()) return;
    this.isDetecting.set(true);
    this.resultado.set('Iniciando detección en tiempo real...');
    this.status.set(null);

    const tick = async () => {
      if (this.busy) return;
      this.busy = true;
      try {
        await this.captureAndSendFrame();
      } catch (e) {
        console.error(e);
      } finally {
        this.busy = false;
      }
    };

    tick();
    this.intervalId = window.setInterval(tick, intervalMs);
  }

  stopRealtimeDetection() {
    if (this.intervalId !== null) {
      window.clearInterval(this.intervalId);
      this.intervalId = null;
    }
    this.isDetecting.set(false);
    this.resultado.set('Detección en tiempo real detenida.');
  }

  private async captureAndSendFrame() {
    const video = this.videoEl.nativeElement;
    const canvas = this.canvasEl.nativeElement;

    if (!video.videoWidth || !video.videoHeight) {
      console.warn('Video no tiene dimensiones.');
      return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const blob: Blob = await new Promise(resolve => canvas.toBlob(b => resolve(b as Blob), 'image/jpeg', 0.8));

    const prev = this.preview();
    if (prev && typeof prev === 'string' && prev.startsWith('blob:')) {
      URL.revokeObjectURL(prev);
    }
    this.preview.set(URL.createObjectURL(blob));

    const formData = new FormData();
    formData.append('file', blob, 'frame.jpg');

    try {
      const res = await fetch(this.detectUrl, { method: 'POST', body: formData });
      if (!res.ok) {
        console.error('Error API:', await res.text());
        this.resultado.set('❌ Error de red en tiempo real.');
        return;
      }
      const json = (await res.json()) as DetectionStatus;
      this.status.set(json);
      this.resultado.set(json.message);
      this.annotatedImageUrl.set(null);      this.updateStatistics(json.safe);

      if (json.safe === false) {
        this.playAlertSound();
        await this.sendWhatsAppAlert('⚠️ ALERTA: Persona sin casco detectada en tiempo real.');
      }

    } catch (error) {
      console.error('Error en la detección de frame', error);
      this.resultado.set('❌ Error de conexión al servidor.');
    }
  }

  ngOnDestroy(): void {
    this.stopRealtimeDetection();
    this.stopCamera();
    const ann = this.annotatedImageUrl();
    if (ann) URL.revokeObjectURL(ann);
    const prev = this.preview();
    if (prev && typeof prev === 'string' && prev.startsWith('blob:')) {
      URL.revokeObjectURL(prev);
    }
  }
}

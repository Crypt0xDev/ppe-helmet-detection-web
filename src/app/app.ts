import { NgClass, NgIf } from '@angular/common';
import { ChangeDetectionStrategy, Component, ElementRef, OnDestroy, ViewChild, signal } from '@angular/core';
import { environment } from '../environments/environment';

interface DetectionStatus {
  status_message: string;
  safe: boolean;
  helmet_count: number;
  head_count: number;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [NgIf, NgClass],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnDestroy {
  mode = signal<'selection' | 'upload' | 'realtime'>('selection');

  preview = signal<string | ArrayBuffer | null>(null);
  resultado = signal<string | null>(null);
  imagen = signal<File | null>(null);

  @ViewChild('videoEl') videoEl!: ElementRef<HTMLVideoElement>;
  @ViewChild('canvasEl') canvasEl!: ElementRef<HTMLCanvasElement>;
  private stream: MediaStream | null = null;
  private intervalId: number | null = null;
  private busy = false;

  detectUrl = `${environment.apiUrl}/detect/`;
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

    this.resultado.set('⏳ Procesando...');
    this.status.set(null);
    this.annotatedImageUrl.set(null);

    try {
      const formData = new FormData();
      formData.append('file', currentImagen);

      const resJson = await fetch(this.detectUrl, { method: 'POST', body: formData });
      if (!resJson.ok) {
        const error = await resJson.text();
        this.resultado.set(`❌ Error en la API: ${error}`);
        return;
      }

      const json = (await resJson.json()) as DetectionStatus;
      this.status.set(json);
      this.resultado.set(json.status_message);
      // Enviar alerta si hay riesgo
if (json.safe === false) {
  await this.sendWhatsAppAlert("⚠️ ALERTA: Persona sin casco detectada.");
}


      const formData2 = new FormData();
      formData2.append('file', currentImagen);
      const resImage = await fetch('http://localhost:8000/detect/image', { method: 'POST', body: formData2 });

      if (resImage.ok) {
        const blob = await resImage.blob();
        const prevUrl = this.annotatedImageUrl();
        if (prevUrl) URL.revokeObjectURL(prevUrl);
        this.annotatedImageUrl.set(URL.createObjectURL(blob));
      }
    } catch (e) {
      console.error('Error al enviar imagen:', e);
      this.resultado.set('❌ Error de conexión con la API.');
    }
  }

  async startCamera() {
    if (this.isCameraOn()) return;
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: false });
      const video = this.videoEl.nativeElement;
      video.srcObject = this.stream;
      await video.play();
      this.isCameraOn.set(true);
      this.resultado.set('Cámara encendida. ¡Lista para detección!');
      this.status.set(null);
      this.annotatedImageUrl.set(null);
    } catch (e) {
      console.error('No se pudo iniciar la cámara', e);
      this.isCameraOn.set(false);
      this.resultado.set('❌ Permiso de cámara denegado o no disponible.');
    }
  }
/*HDFKJSKFJHSDKJFHSKDFH */
  async sendWhatsAppAlert(message: string) {
  try {
    const res = await fetch(`${environment.apiUrl}/alert/whatsapp`, {
      method: 'POST',
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: message
      })
    });

    if (!res.ok) {
      console.error("Error al enviar alerta:", await res.text());
    } else {
      console.log("Alerta WhatsApp enviada correctamente.");
    }
  } catch (err) {
    console.error("Error WhatsApp:", err);
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
      this.resultado.set(json.status_message);
      this.annotatedImageUrl.set(null);
      // Alerta automática en tiempo real
if (json.safe === false) {
  await this.sendWhatsAppAlert("⚠️ ALERTA EN TIEMPO REAL: Persona sin casco detectada.");
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

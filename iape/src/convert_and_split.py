#!/usr/bin/env python3
"""
convert_and_split.py
Convierte anotaciones PascalVOC (XML) -> YOLO txt, divide dataset en train/val y copia imágenes.
Uso:
    python convert_and_split.py --dataset ~/iape/hard-hat-detection --train-ratio 0.8
"""

import os
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
import random
import shutil
from tqdm import tqdm

# Mapea nombres de las etiquetas en los XML a índices YOLO (ajusta aquí si quieres otros nombres)
CLASS_MAP = {
    "head": 0,
    "helmet": 1,
    # si quieres agregar 'person' u otros: "person": 2,
}

def xml_to_yolo(xml_path, class_map):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    size = root.find('size')
    if size is None:
        raise ValueError(f"No size tag in {xml_path}")
    w = float(size.find('width').text)
    h = float(size.find('height').text)

    yolo_objs = []
    for obj in root.findall('object'):
        name = obj.find('name').text.strip()
        if name not in class_map:
            # ignorar clases no mapeadas
            continue
        cls_id = class_map[name]
        bnd = obj.find('bndbox')
        xmin = float(bnd.find('xmin').text)
        ymin = float(bnd.find('ymin').text)
        xmax = float(bnd.find('xmax').text)
        ymax = float(bnd.find('ymax').text)
        # convertir a formato YOLO (x_center, y_center, w, h) normalizados
        x_center = (xmin + xmax) / 2.0 / w
        y_center = (ymin + ymax) / 2.0 / h
        bw = (xmax - xmin) / w
        bh = (ymax - ymin) / h
        # evitar valores fuera de rango por redondeo
        x_center = max(min(x_center, 1.0), 0.0)
        y_center = max(min(y_center, 1.0), 0.0)
        bw = max(min(bw, 1.0), 0.0)
        bh = max(min(bh, 1.0), 0.0)
        yolo_objs.append((cls_id, x_center, y_center, bw, bh))
    return yolo_objs

def main(dataset_dir, train_ratio):
    dataset_dir = Path(dataset_dir).expanduser()
    ann_dir = dataset_dir / "annotations"
    img_dir = dataset_dir / "images"

    if not ann_dir.exists():
        raise SystemExit(f"No existe {ann_dir}")
    if not img_dir.exists():
        raise SystemExit(f"No existe {img_dir}")

    out_images_train = dataset_dir / "images_train"
    out_images_val = dataset_dir / "images_val"
    out_labels_train = dataset_dir / "labels_train"
    out_labels_val = dataset_dir / "labels_val"

    for p in [out_images_train, out_images_val, out_labels_train, out_labels_val]:
        p.mkdir(exist_ok=True)

    xml_files = sorted(list(ann_dir.glob("*.xml")))
    if len(xml_files) == 0:
        raise SystemExit("No se encontraron archivos XML en annotations/")

    random.shuffle(xml_files)
    split_index = int(len(xml_files) * train_ratio)
    train_files = xml_files[:split_index]
    val_files = xml_files[split_index:]

    print(f"Total XML: {len(xml_files)} -> train: {len(train_files)}, val: {len(val_files)}")

    # Procesar función
    def process_list(file_list, images_out, labels_out):
        for xml_file in tqdm(file_list):
            tree = ET.parse(xml_file)
            root = tree.getroot()
            filename_tag = root.find('filename')
            if filename_tag is None:
                # intenta deducir nombre
                base = xml_file.stem
                # añade posible extension .jpg/.png
                # pero primero buscar en images dir
                fname = None
                for ext in ['.jpg', '.jpeg', '.png', '.JPG', '.PNG']:
                    cand = img_dir / (base + ext)
                    if cand.exists():
                        fname = cand.name
                        break
                if not fname:
                    print(f"Warn: no filename in {xml_file} y no se encontró imagen candidata para {xml_file.stem}")
                    continue
            else:
                fname = filename_tag.text.strip()

            # ruta origen imagen
            src_img = img_dir / fname
            if not src_img.exists():
                # intentar con .png/.jpg si filename no contiene extension
                if src_img.suffix == '':
                    found = False
                    for ext in ['.jpg', '.jpeg', '.png', '.JPG', '.PNG']:
                        cand = img_dir / (src_img.name + ext)
                        if cand.exists():
                            src_img = cand
                            found = True
                            break
                    if not found:
                        print(f"Imagen no encontrada para {xml_file}: buscada {src_img}")
                        continue
                else:
                    print(f"Imagen no encontrada: {src_img}")
                    continue

            # convertir annotations a yolo
            yolo_objs = xml_to_yolo(xml_file, CLASS_MAP)
            # escribir archivo de label
            label_path = labels_out / (src_img.stem + ".txt")
            with open(label_path, "w") as f:
                for (cls_id, xc, yc, bw, bh) in yolo_objs:
                    f.write(f"{cls_id} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}\n")

            # copiar imagen
            dst_img = images_out / src_img.name
            shutil.copy2(src_img, dst_img)

    # procesar
    process_list(train_files, out_images_train, out_labels_train)
    process_list(val_files, out_images_val, out_labels_val)

    print("Conversión completada.")
    print(f"Train images -> {out_images_train}  labels -> {out_labels_train}")
    print(f"Val   images -> {out_images_val}    labels -> {out_labels_val}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", "-d", required=True, help="Ruta al dataset (carpeta que contiene annotations/ y images/)")
    parser.add_argument("--train-ratio", "-r", type=float, default=0.8, help="Fracción para train (default 0.8)")
    args = parser.parse_args()
    main(args.dataset, args.train_ratio)

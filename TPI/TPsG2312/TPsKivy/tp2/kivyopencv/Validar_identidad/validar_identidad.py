from deepface import DeepFace
import os


def validar_identidad():
    carpeta_imagenes = "usuarios"

    archivos = os.listdir("usuarios")

    imagen_referencia = "captured_image.jpg"

    for archivo in archivos:
        imagen_actual = os.path.join("usuarios", archivo)

        try: 
            validacion = DeepFace.verify(img1_path=imagen_referencia, img2_path=imagen_actual)["verified"]
            if DeepFace.verify(img1_path=imagen_referencia, img2_path=imagen_actual)["verified"]:
                return True
        except Exception as e:
            print()
    return False

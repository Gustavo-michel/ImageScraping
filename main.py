import os
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def download_images(query, num_images):
    """Selenium download Query

    Args:
        query (String): Name of query.
        num_images (Int): Number of images to search
    """

    # Create dir
    folder_name = query.replace(" ", "_")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Search
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/imghp")

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    
    image_urls = set()

    # Find Links
    while len(image_urls) < num_images:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            images = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "g-img img"))
            )
        except TimeoutException as e:
            print(f"Erro: {e}")

        for image in images:
            src = image.get_attribute("src")
            if src:
                image_urls.add(src)

    # Save images
    for i, url in enumerate(image_urls):
        if i >= num_images:
            break
        try:
            image_path = os.path.join(folder_name, f"{query.replace(' ', '_')}_{i+1}.jpg")
            urllib.request.urlretrieve(url, image_path)
            print(f"Imagem salva: {image_path}")
        except Exception as e:
            print(f"Erro ao salvar a imagem {i+1}: {e}")

    driver.quit()

def init_query():
    """Init Tkinter entries for Query

    """
    query = entry_query.get()
    num_images = entry_num.get()
    
    if not query or not num_images:
        CTkMessagebox(title="Campos vazios", message="Por favor, preencha todos os campos")
        return

    try:
        num_images = int(num_images)
    except ValueError:
        CTkMessagebox(title="Entrada inválida", message="A quantidade de imagens deve ser um número inteiro")
        return

    download_images(query, num_images)
    CTkMessagebox(title="Concluído", message="Download de imagens concluído!")

# Tkinter Interface
window = ctk.CTk()
window.title("Google Image Downloader")
window.geometry("500x350")
window.minsize(200,315)
window.iconbitmap("Logo.ico")

label_query = ctk.CTkLabel(window, text="To search:")
label_query.pack(padx=10, pady=10)
entry_query = ctk.CTkEntry(window, width=200)
entry_query.pack(padx=10, pady=10)

label_num = ctk.CTkLabel(window, text="Number of images:")
label_num.pack(padx=10, pady=10)
entry_num = ctk.CTkEntry(window, width=50)
entry_num.pack(padx=10, pady=10)

button_download = ctk.CTkButton(window, text="Download images", command=init_query, fg_color="#a70fff", hover_color="#730bb0")
button_download.pack(padx=10, pady=50)

window.mainloop()

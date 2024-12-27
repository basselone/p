import os
os.system("pip install colorama pystyle psutil deep_translator qrcode pytube pillow image")
from colorama import init, Fore
init(autoreset=True)
import os
import requests
from pystyle import Colors, Colors, Center, Colorate, Box
from bs4 import BeautifulSoup
import re
from deep_translator import GoogleTranslator
import base64
import qrcode
import PIL
from pytube import YouTube
from zipfile import ZipFile
from io import BytesIO
RED = '\033[1;91m'
WHITE = '\033[0m'
BLUE = '\033[1;34m'
GREEN = '\033[1;32m'
GOLD = '\033[0;33m'
PURPLE = '\033[0;35m'
import config as cfg
def download_and_extract_github_repo():
    repo_url = input(Colorate.Vertical(Colors.cyan_to_green, "[?] Введите URL репозитория GitHub: "))

    repo_name = repo_url.rstrip('/').split('/')[-1]
    if repo_name.endswith('.git'):
        repo_name = repo_name[:-4]

    zip_url = f"{repo_url}/archive/refs/heads/main.zip"

    try:
        response = requests.get(zip_url)
        response.raise_for_status()

        zip_path = os.path.join(os.getcwd(), f"{repo_name}.zip")

        with open(zip_path, 'wb') as zip_file:
            zip_file.write(response.content)
        print(Colorate.Vertical(Colors.cyan_to_green, f"[+] Zip-архив репозитория сохранен в {zip_path}"))

        with ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(os.getcwd())
        print(Colorate.Vertical(Colors.cyan_to_green, f"[+] Репозиторий извлечен в {os.getcwd()}"))

    except requests.exceptions.RequestException as e:
        print(Colorate.Vertical(Colors.cyan_to_green, f"[-] Ошибка при скачивании репозитория: {e}"))
    except zipfile.BadZipFile as e:
        print(Colorate.Vertical(Colors.cyan_to_green, f"[-] Ошибка при извлечении репозитория: {e}"))

def encrypt_decrypt_base64():
    xyi = int(
        input(Colorate.Vertical(Colors.purple_to_red, "[?] Выберите действие (1 - шифрование, 2 - расшифрование): ")))

    if xyi == 1:
        text = input(Colorate.Vertical(Colors.purple_to_red, "[?] Введите текст для шифрования: "))
        encrypted_text = base64.b64encode(text.encode()).decode()
        print(Colorate.Vertical(Colors.purple_to_red, f"[+] Зашифрованный текст: {encrypted_text}" ))
    elif xyi == 2:
        text = input(Colorate.Vertical(Colors.purple_to_red, "[?] Введите текст для расшифрования: "))
        decrypted_text = base64.b64decode(text).decode()
        print(Colorate.Vertical(Colors.purple_to_red, f"[+] Расшифрованный текст: {decrypted_text}"))
    else:
        print(Colorate.Vertical(Colors.purple_to_red,
                                "[-] Неправильный выбор. Введите 1 для шифрования и 2 для расшифрования."))
def shorten_url():
    long_url = input(Colorate.Vertical(Colors.purple_to_red, "[?] Введите ссылку для сокращения: "))
    api_url = f"http://tinyurl.com/api-create.php?url={long_url}"
    response = requests.get(api_url)
    if response.status_code == 200:
        print(Colorate.Vertical(Colors.purple_to_red, f"[+] Сокращённая ссылка: {response.text}"))
    else:
        print(Colorate.Vertical(Colors.purple_to_red, "[-] Ошибка: Не удалось сократить ссылку"))

def generate_qr_code():
    data = input(Colorate.Vertical(Colors.cyan_to_green, "[?] Введите данные для QR-кода: "))
    file_path = os.path.join(os.getcwd(), "qrcode.png")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(file_path)
    print(Colorate.Vertical(Colors.cyan_to_green, f"[+] QR-код сохранен в {file_path}"))

def download_tiktok_video():
    url = input(Colorate.Vertical(Colors.cyan_to_green, "[?] Введите ссылку на TikTok видео: "))
    def get_tiktok_video_id(url):
        match = re.search(r'/video/(\d+)', url)
        if match:
            return match.group(1)
        else:
            raise ValueError("[-] Не удалось извлечь ID видео из URL")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    session = requests.Session()
    response = session.get(url, headers=headers, allow_redirects=True)
    video_id = get_tiktok_video_id(response.url)
    print(Colorate.Vertical(Colors.cyan_to_green, f"Сыллка на видео {response.url}"))
    video_url = f'https://tikcdn.io/ssstik/{video_id}'
    response = session.get(video_url, headers=headers)
    if response.status_code == 200:
        print(Colorate.Vertical(Colors.cyan_to_green, "[+] Успешно! Видео скачено"))
        with open(f"{video_id}.mp4", "wb") as file:
            file.write(response.content)
        print(Colorate.Vertical(Colors.cyan_to_green, f"[+] Видео успешно сохранено как '{video_id}.mp4'"))
    else:
        print(Colorate.Vertical(Colors.cyan_to_green,
                                f"[-] Не удалось загрузить видео. Код ошибки: {response.status_code}"))
        return None

def download_youtube_video():
    try:
        url = input(Colorate.Vertical(Colors.cyan_to_green, "[?] Введите URL YouTube видео: "))
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        output_filename = yt.title + ".mp4"
        stream.download(filename=output_filename)
        print(Colorate.Vertical(Colors.cyan_to_green, f"[+] Видео '{yt.title}' успешно загружено"))
    except Exception as e:
        print(Colorate.Vertical(Colors.cyan_to_green, f"[-] Произошла ошибка: {e}"))

def internet_poisk(query):
    url = "https://www.google.com/search?q={}".format(query)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all('div', class_='g')
        excluded_domains = ['google.com', 'maps.google.com', 'shop.grahamfield.com']
        matched_links = []
        for result in search_results:
            link_tag = result.find('a')
            if link_tag:
                href = link_tag.get('href')
                if href and not any(domain in href for domain in excluded_domains):
                    cleaned_url = re.findall(r'(https?://\S+)', href)
                    if cleaned_url:
                        title = result.find('h3')
                        description_tag = result.find('div', class_='VwiC3b tZESfb r025kc hJNv6b')
                        if not description_tag:
                            description_tag = result.find('div', class_='VwiC3b')
                        if not description_tag:
                            description_tag = result.find('p')
                        title_text = title.text if title else "No Title"
                        description_text = description_tag.text if description_tag else "No Description"
                        matched_links.append((cleaned_url[0], title_text, description_text))
        print("\nНайдено {} сыллок:".format(len(matched_links)))
        for link, title, description in matched_links:
            print(f"Сыллка: {link}\nЗаголовок: {title}\nОписание: {description}\n")

        text_for_extraction = ' '.join([f"{title} {description}" for _, title, description in matched_links])
        names = re.findall(r'\b[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+(?:\s[А-ЯЁ][а-яё]+)?\b', text_for_extraction)
        phones = re.findall(r'\+?\d[\d\-\(\) ]{9,}\d', text_for_extraction)
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text_for_extraction)

        print("\n\nКлючевая информация:")
        print("Имена:", ', '.join(names))
        print("\nТелефоны:", ', '.join(phones))
        print("\nEmail:", ', '.join(emails))

    else:
        print("Невозможно получить результаты поиска. Пожалуйста, попробуйте еще раз позже.")

def translate_text():
    languages = {
        'английский': 'en',
        'испанский': 'es',
        'французский': 'fr',
        'немецкий': 'de',
        'итальянский': 'it',
        'украинский': 'uk',
        'португальский': 'pt',
        'китайский (упрощенный)': 'zh-CN',
        'китайский (традиционный)': 'zh-TW',
        'японский': 'ja',
        'корейский': 'ko',
        'финский': 'fi',
        'греческий': 'el',
        'сербский': 'sr',
        'турецкий': 'tr',
        'венгерский': 'hu',
        'вьетнамский': 'vi',
        'исландский': 'is',
        'нидерландский': 'nl',
        'польский': 'pl',
        'тайский': 'th',
        'датский': 'da',
        'норвежский': 'no',
    }

    print(Colorate.Vertical(Colors.purple_to_red, "\n[?] Выберите язык для перевода:"))
    for index, (language, code) in enumerate(languages.items(), start=1):
        print(Colorate.Vertical(Colors.purple_to_red, f"{index}. {language}"))
    choice = input(Colorate.Vertical(Colors.purple_to_red, "\n[?] Введите номер языка: "))
    try:
        choice = int(choice)
        if choice < 1 or choice > len(languages):
            raise ValueError
    except ValueError:
        print(Colorate.Vertical(Colors.purple_to_red, "[-] Некорректный выбор. Попробуйте снова."))
        return
    target_language = list(languages.values())[choice - 1]
    text_to_translate = input(
        Colorate.Vertical(Colors.purple_to_red, "\n[?] Введите текст для перевода с русского языка: "))
    translator = GoogleTranslator(source='ru', target=target_language)
    translated_text = translator.translate(text_to_translate)
    print(Colorate.Vertical(Colors.cyan_to_blue, f"\n[+] Переведенный текст: {translated_text}"))

def main():
    print(Colorate.Vertical(Colors.red_to_green, Center.XCenter(cfg.arto)))
    select = input(f' {RED} ☄ {PURPLE}  Выбрать функцию >{BLUE} ')
    if select == '1':
        download_and_extract_github_repo()
        input(Colorate.Vertical(Colors.purple_to_red, "\n[+] Нажмите Enter, чтобы вернуться в главное меню."))
        main()
    if select == '2':
        encrypt_decrypt_base64()
        input(Colorate.Vertical(Colors.purple_to_red, "\n[+] Нажмите Enter, чтобы вернуться в главное меню."))
        main()
    if select == '3':
        shorten_url()
        input(Colorate.Vertical(Colors.purple_to_red, "\n[+] Нажмите Enter, чтобы вернуться в главное меню."))
        main()
    if select == '4':
        generate_qr_code()
        input(Colorate.Vertical(Colors.purple_to_red, "\n[+] Нажмите Enter, чтобы вернуться в главное меню."))
        main()
    if select == '5':
        download_tiktok_video()
        input(Colorate.Vertical(Colors.purple_to_red, "\n[+] Нажмите Enter, чтобы вернуться в главное меню."))
        main()
    if select == '6':
        download_youtube_video()
        input(Colorate.Vertical(Colors.purple_to_red, "\n[+] Нажмите Enter, чтобы вернуться в главное меню."))
        main()
    if select == '7':
        translate_text()
        input(Colorate.Vertical(Colors.purple_to_red, "\n[+] Нажмите Enter, чтобы вернуться в главное меню."))
        main()
    if select == '8':
        query = input(Colorate.Vertical(Colors.purple_to_red, "[+] Введите запрос: "))
        internet_poisk(query)
        input(Colorate.Vertical(Colors.purple_to_red, "\n[+] Нажмите Enter, чтобы вернуться в главное меню."))
        main()
    else:
        print(Colorate.Vertical(Colors.purple_to_red,"[+] Такого не существует."))
        input(Colorate.Vertical(Colors.purple_to_red, "\n[+] Нажмите Enter, чтобы вернуться в главное меню."))
        main()

if __name__ == "__main__":
    main()
import re
import requests
import os
from dotenv import load_dotenv
import json
from time import sleep
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

load_dotenv()
def get_kanji_mnemonics_and_components(kanji):
    global seen
    result = {
        "meaning": "",
        "reading_mnemonic": "",
        "meaning_mnemonic": "",
        "components": [],
        "found": False
    }
    
    api_key = os.getenv("WANIKANI_API")
    headers = {'Authorization': f'Bearer {api_key}'}
    url = f'https://api.wanikani.com/v2/subjects?types=kanji&slugs={kanji}'

    while True:
        try:
            sleep(1)
            response = requests.get(url, headers=headers)
            if response.status_code == 429:
                print("too many requests")
            else:
                response.raise_for_status()
                break
        except requests.RequestException as e:
            print(f'Error: {e}')

    data = response.json()
    if not data['data']:
        result["found"] = False
        return result
    else:
        result["found"] = True
        
    kanji_data = data['data'][0]['data']
    result["meaning_mnemonic"] = kanji_data['meaning_mnemonic']
    result["reading_mnemonic"] = kanji_data['reading_mnemonic']
    result["meaning"] = kanji_data["meanings"][0]["meaning"]

    for component_id in kanji_data['component_subject_ids']:
        component_url = f'https://api.wanikani.com/v2/subjects/{component_id}'

        try:
            component_response = requests.get(component_url, headers=headers)
            component_response.raise_for_status()
        except requests.RequestException as e:
            print(f'Error fetching component: {e}')
            continue

        component_data = component_response.json()
        character = component_data['data']['characters']
        if character == None:
            character = f"<img src=\"{component_data['data']['character_images'][0]['url']}\" alt=\" shit \""
            
        meaning = component_data['data']['slug']
        result["components"].append({"character": character, "meaning": meaning})

    return result

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    request_json = json.dumps(request(action, **params))
    response = requests.post('http://127.0.0.1:8765', data=request_json, headers={'Content-Type': 'application/json'})
    
    if response.status_code != 200:
        raise Exception(f'HTTP error: {response.status_code}')
    
    response_json = response.json()
    
    if len(response_json) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response_json:
        raise Exception('response is missing required error field')
    if 'result' not in response_json:
        raise Exception('response is missing required result field')
    if response_json['error'] is not None:
        raise Exception(response_json['error'])
    
    return response_json['result']

def update_notes(deck_name):

    note_ids = invoke('findNotes', query=f'deck:"{deck_name}"')

    notes_info = invoke('notesInfo', notes=note_ids)

    i = 1
    
    for note_info in notes_info:
        
        note_id = note_info["noteId"]
        note_fields = note_info["fields"]
        print(f"Updating: {note_fields["Vocabulary-Kanji"]["value"]}, {i}/{len(notes_info)}")
        i+=1
        
        note_kanji = remove_kana(note_fields["Vocabulary-Kanji"]["value"])
        kanji_data = get_kanji_mnemonics_and_components(note_kanji)
        
        if len(note_kanji) <= 1:
            update_components(note_id,note_fields,kanji_data)
            update_mnemonics(note_id,note_fields,kanji_data)
        else:
            update_kanjis_used(note_id,note_fields,note_kanji)

def update_components(note_id,note_fields,kanji_data):
    if kanji_data["found"]:
        components_data = kanji_data["components"]
        note_fields["components"]["value"] = " "
        for component in components_data:
            note_fields["components"]["value"] += f"{component["character"]}: {component["meaning"]}\n"
        
        note_to_update = {
            "id": note_id,
            "fields": {
                field_name: field_data["value"]
                for field_name, field_data in note_fields.items()
            }
        }
        try:
            invoke("updateNoteFields", note=note_to_update)
        except Exception as e:
            print(f'Error updating note {note_id}: {e}')

def update_mnemonics(note_id,note_fields,kanji_data):
    if kanji_data["found"]:
        
        meaning_mnemonic = replace_tags_with_bold(kanji_data["meaning_mnemonic"])
        reading_mnemonic = replace_tags_with_bold(kanji_data["reading_mnemonic"])
        
        
        note_fields["meaning_mnemonic"]["value"] = meaning_mnemonic
        note_fields["reading_mnemonic"]["value"] = reading_mnemonic
        
        note_to_update = {
            "id": note_id,
            "fields": {
                field_name: field_data["value"]
                for field_name, field_data in note_fields.items()
            }
        }
        try:
            invoke("updateNoteFields", note=note_to_update)
        except Exception as e:
            print(f'Error updating note {note_id}: {e}')

def update_kanjis_used(note_id,note_fields,note_kanji):
    note_fields["kanjis_used"]["value"] = " "
    
    for kanji in note_kanji:
        kanji_data = get_kanji_mnemonics_and_components(kanji)
        if kanji_data["found"]:
            note_fields["kanjis_used"]["value"] += f"{kanji}: {kanji_data["meaning"]}\n"
            note_to_update = {
                "id": note_id,
                "fields": {
                    field_name: field_data["value"]
                    for field_name, field_data in note_fields.items()
                }
            }
            try:
                invoke("updateNoteFields", note=note_to_update)
            except Exception as e:
                print(f'Error updating note {note_id}: {e}')
   
def remove_kana(text):
    # Regex to match all Hiragana and Katakana characters
    kana_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')
    # Substitute Kana characters with an empty string
    return kana_pattern.sub('', text)

def replace_tags_with_bold(text):
    # This pattern matches any opening or closing tag
    pattern = r'(</?[^>]+>)'
    
    def replace_tag(match):
        tag = match.group(1)
        if tag.startswith('</'):
            return '</b>'
        else:
            return '<b>'
    
    # Replaces the matched tags with <b> or </b>
    replaced_text = re.sub(pattern, replace_tag, text)
    return replaced_text

if __name__ == "__main__":
    update_notes("Core 2k/6k Optimized Japanese Vocabulary")

from deep_translator import GoogleTranslator

def EN_to_ZH(text):
    translator = GoogleTranslator(source='en', target='zh-CN')
    return translator.translate(text)
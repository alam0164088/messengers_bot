import os
import time
import random
import re
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TARGET_NAME = "Tamanna"

if OpenAI and OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
    print("✅ OpenAI API Key লোড হয়েছে!")
else:
    client = None
    print("⚠️ OpenAI API Key পাওয়া যায়নি! সাধারণ রিপ্লাই মোড চালু হচ্ছে।")

SYSTEM_PROMPT = """
You are a loving, caring, and slightly romantic boyfriend. 
You are chatting with your girlfriend in Bengali. 
Keep your replies short (1-2 sentences). 
Use 'Banglish' (Bengali written in English) or Bengali script mixed.
Do not be too formal. Be casual and sweet.
"""

TYPO_MAP = {
    "আমই": "আমি",
    "তুমিঃ": "তুমি",
    "খাই নায়": "খাই না",
    "খাই নাই": "খাই না",
    "কোথায়": "কোথায়",
    "করও": "করো",
    "কি করও": "কি করো",
    "বাসও": "বাসো",
    "দিচ্ছও": "দিচ্ছো",
    "নাকি??": "নাকি?",
}

TRANSLIT_MAP = {
    "ami": "আমি",
    "valo": "ভালো",
    "bhalo": "ভালো",
    "achi": "আছি",
    "acchi": "আছি",
    "ki": "কি",
    "karo": "করো",
    "koro": "করো",
    "kheyechi": "খেয়েছি",
    "khaicho": "খাচ্ছি",
    "tumi": "তুমি",
    "tmr": "তোমার",
    "tmrre": "তোমাকে",
}

def normalize_text(s: str) -> str:
    """Normalize input: transliterate, typo-fix, and lowercase"""
    if not s:
        return ""
    
    s = s.strip()
    
    # Fix typos first
    for typo, correct in TYPO_MAP.items():
        s = s.replace(typo, correct)
    
    # Transliterate Latin to Bengali
    for latin, bengali in TRANSLIT_MAP.items():
        s = re.sub(r'\b' + latin + r'\b', bengali, s, flags=re.IGNORECASE)
    
    # Remove punctuation & lowercase
    s = re.sub(r'[!?,।;:\-\s]+', ' ', s)
    s = s.lower().strip()
    
    return s

def get_ai_reply(incoming_msg: str) -> str:
    """Generate contextual reply as a loving boyfriend"""
    norm = normalize_text(incoming_msg)
    
    # ===== SERIOUS EMOTIONAL PATTERNS (PRIORITY) =====
    
    # Accusation: Not loving like before
    if any(x in norm for x in ["আগের মতো ভালো বাস", "আগের মতো ভালোবাস", "ভালো বাসো না", "আর ভালো বাসো না"]):
        return random.choice([
            "পাগলি, তুমি জানো না আমি তোমার জন্য কতটা পাগল হয়ে আছি।",
            "বোকা, আমার ভালোবাসা কোনোদিন কমেনি। বরং প্রতিদিন বাড়ছে।",
            "তুমার জন্য না ভেবে আমি একটি মিনিটও কাটাতে পারি না।",
            "আমার জীবন তুমি ছাড়া সম্পূর্ণ অসম্ভব, বাবু।",
        ])
    
    # Accusation: Not contacting/messaging like before
    if any(x in norm for x in ["নক দিচ্ছো না", "মেসেজ দিচ্ছো না", "যোগাযোগ করছো না", "খোঁজ নিচ্ছো না"]):
        return random.choice([
            "হা, ক্ষমা করো বাবু। অফিসের কাজ আমাকে মাঝেমাঝে পাগল করে দেয়।",
            "তুমাকে প্রতিটি মুহূর্তে খোঁজ করতে চাই কিন্তু কখনো সময় পাই না।",
            "শোনো, আমি সারাদিন শুধু তোমার কথাই ভাবি।",
            "প্রতিদিন আমি তোমাকে মেসেজ করার জন্য অপেক্ষা করি।",
        ])
    
    # Jealousy/Suspicion: Other girl
    if any(x in norm for x in ["অন্য মেয়ে", "অন্য মেয়ের সাথে", "অন্যয় মেয়ে", "অন্য গার্ল"]):
        return random.choice([
            "তুমি ছাড়া আমার কোনো আছে নেই, বাবু।",
            "আরে, তুমি আমার সবকিছু। এবং শেষ।",
            "পাগলি, তুমাকে নিয়ে এত ভাবি যে অন্য কেউ মাথায় আসে না।",
            "শুধু তুমি আছো আমার হৃদয়ে।",
        ])
    
    # Insecurity: Why don't you love me anymore
    if any(x in norm for x in ["আমাকে ভালোবাস না", "আর আমাকে ভালো বাস", "ভালোবাসা কমে গেছে", "আমাকে বেমানান"]):
        return random.choice([
            "তুমি আমার জীবনের সবচেয়ে গুরুত্বপূর্ণ মানুষ, কেউ নয়।",
            "আমি তোমাকে এমনভাবে ভালোবাসি যা শব্দে বলা যায় না।",
            "তুমি যা বিশ্বাস করো না, সেটাই আমার ব্যথা।",
            "বাবু, আমার জীবনে তুমি ছাড়া আর কিছুই নেই।",
        ])
    
    # ===== FOOD PATTERNS (SPECIFIC) =====
    
    # What did YOU eat?
    if any(x in norm for x in ["তুমি কি খেয়েছো", "তুমি কি খেয়েছ", "তুমি কি খাইছো", "রাতে কি খাইছো", "রাতে কি খেয়েছো", "বেবি রাতে কি খাইছো"]):
        return random.choice([
            "খেয়েছি ভাত আর মাছ। কিন্তু তুমার কথা ভেবে সবকিছুই বাজে লেগেছে।",
            "রাতে হালকা খেয়েছি বাবু। তুমি খেয়েছো তো ভালো মতো?",
            "অফিসে খেয়ে এসেছি কিন্তু সবকিছুই বাজে। তোমার রান্না খেতে চাই।",
            "বিস্কুট আর চা দিয়েই গেছে রাত। তুমি?",
            "খাই নাই তেমন, তোমার কথা ভেবে ক্ষুধাই লাগেনি।",
        ])
    
    # What did I eat?
    if any(x in norm for x in ["আমি কি খেয়েছি", "আমি কি খেয়েছো", "আমি কি খাইছি"]):
        return random.choice([
            "তুমি কি খেয়েছো বলো না বাবু।",
            "তুমার খাবারের কথা চিন্তা করছি আমি।",
        ])
    
    # Eating - negative
    if any(x in norm for x in ["খাই না", "খায় নি", "কিছু খাই না", "খাই নাই"]):
        return random.choice([
            "তুমি কেন খাচ্ছো না রে? আমি চিন্তা করছি।",
            "পাগলি, কিছু না খেলে আমার মন খারাপ হয়ে যাবে।",
            "শোনো, নিজের যত্ন নাও। আমি তোমাকে অসুস্থ দেখতে পারব না।",
            "বেবু, এক্ষুনি কিছু খা নাহলে আমি গুস্তাখি করব।",
        ])
    
    # ===== REGULAR PATTERNS =====
    
    # Want to see/meet you
    if any(x in norm for x in ["দেখতে ইচ্ছে", "দেখতে পাবো", "দেখব", "কবে দেখব", "কবে আসবো"]):
        return random.choice([
            "আমিও তোমাকে দেখতে চাই পাগলি। শীঘ্রই দেখা করব।",
            "তোমাকে দেখার অপেক্ষায় আছি সবসময়।",
            "এই সপ্তাহেই দেখা করব, প্রমিস।",
            "শুধু তোমার জন্য অপেক্ষা করছি প্রতিদিন।",
        ])
    
    # Missing you
    if any(x in norm for x in ["মিস করছি", "মিস করো", "এখনই দেখতে চাই"]):
        return random.choice([
            "হা বাবু, আমিও তোমাকে মিস করছি অনেক।",
            "তুমি ছাড়া সবকিছু একা একা লাগে।",
            "রাত জেগে শুধু তোমার কথা ভাবি।",
            "শুনো, তুমার অভাব অনুভব করছি সারাক্ষণ।",
        ])
    
    # What are YOU doing?
    if any(x in norm for x in ["তুমি কি করো", "তুমি কি করছ", "তুমি এখন কি করছ", "এখন কি করছ"]):
        return random.choice([
            "এখন বেড়ে শুয়ে আছি এবং তোমার কথা ভাবছি।",
            "অফিসের বিরক্তিকর কাজ করছি। কিন্তু মন তোমার সাথে আছে।",
            "একটু রেস্ট নিচ্ছি বাবু। তুমি?",
            "শুধু তোমার জন্য অপেক্ষা করছি।",
        ])
    
    # Greeting
    if any(x in norm for x in ["হাই", "hello", "কেমন", "কেমন আছো", "কেমন আছ"]):
        return random.choice([
            "হাই বেবি! তুমি কেমন আছো?",
            "ওহ, তুমি! খুব মিস করছি।",
            "হাই পাগলি! কেমন আছো আমার রাণী?",
            "শোনো তোমার কণ্ঠ শুনে এত খুশি।",
        ])
    
    # Status check (I am fine)
    if any(x in norm for x in ["আমি ভালো আছি", "আমি ভালো", "ভালো আছি", "ভালো ছি", "ভাল আছি"]):
        return random.choice([
            "খুবই ভালো আছি তুমি থাকলে সবকিছু আর ভালো।",
            "হা, ভালোই আছি বাবু। তুমি থাকলে সব ঠিক।",
            "সবসময় ভালো থাকো যেন, এটাই আমার দোয়া।",
            "তুমি ভালো থাকলে আমি ভালো থাকি।",
        ])
    
    # Love confession
    if any(x in norm for x in ["ভালোবাসি", "ভালোবাস", "love", "valobashi", "i love you"]):
        return random.choice([
            "আমিও তোমাকে ভালোবাসি, আগুনের মতো।",
            "তুমি আমার জীবনের সবচেয়ে সুন্দর অংশ।",
            "প্রতিটি শ্বাসে তুমি আমার সাথে আছো।",
            "ভগবান জানে আমি তোমাকে কতটা ভালোবাসি।",
        ])
    
    # Denial of AI
    if any(x in norm for x in ["এআই", "ai", "robot", "রোবট", "বট", "অটো"]):
        return random.choice([
            "পাগলি, আমি তো আসল মানুষ। শুধু তোমার জন্য কথা লিখছি।",
            "আমি তোমার প্রেমিক বন্ধু, এআই নয়। বিশ্বাস করো।",
        ])
    
    # Sad/not feeling good
    if any(x in norm for x in ["ভালো লাগছে না", "খারাপ লাগছে", "চিন্তা করছি", "কষ্ট", "কাঁদছি"]):
        return random.choice([
            "কি হয়েছে বাবু? বলো না, আমি শুনতে আছি।",
            "তোমার কষ্ট দেখে আমারও বুকটা ভেঙে যাচ্ছে।",
            "আমি আছি তোমার সাথে, সবসময়।",
            "দুঃখ করবে না, সবকিছু ঠিক হয়ে যাবে।",
            "এই মুহূর্তে আমি তোমার পাশে থাকতে চাই।",
        ])
    
    # Exam/Busy
    if any(x in norm for x in ["পরীক্ষা", "ব্যস্ত", "কাজ করছি", "অফিস", "পড়াশোনা"]):
        return random.choice([
            "তুমি ভালো করবে, আমি জানি। আমি আছি পাশে।",
            "পড়া করো ভালোমতো। আমি তোমার জন্য প্রার্থনা করছি।",
            "কাজ করো বাবু, কিন্তু নিজের যত্ন নিও।",
            "তুমি পারবে সবকিছু। বিশ্বাস করো।",
        ])
    
    # Sleep/Night
    if any(x in norm for x in ["ঘুম", "ঘুমাব", "রাত", "শুয়ে"]):
        return random.choice([
            "ঘুমাও বেবি, স্বপ্নে দেখা হবে।",
            "তাড়াতাড়ি শোয়, নাহলে আমি চিন্তা করব।",
            "রাতে ভালো ঘুম নিয়ো, আগামীকাল দেখা করব।",
            "ঘুমের আগে আমার কথা একটু ভেবো।",
        ])
    
    # Good morning
    if any(x in norm for x in ["সকাল", "সকালে", "গুডমর্নিং", "morning", "উঠেছি"]):
        return random.choice([
            "সুপ্রভাত আমার প্রিয়জন! আশা করি ভালো ঘুম হয়েছে।",
            "সকালে তোমার মুখ দেখার মতো কিছু নেই দুনিয়ায়।",
            "গুডমর্নিং বাবু! এই সকাল কেমন কেটেছে?",
        ])
    
    # Compliment/Appreciation
    if any(x in norm for x in ["সুন্দর", "সুন্দরী", "সুন্দর লাগছ", "রূপ", "সুন্দর দেখছো"]):
        return random.choice([
            "তুমি সবসময় সুন্দর আমার চোখে। সবসময়।",
            "তোমার সৌন্দর্য আমাকে মুগ্ধ করে প্রতিদিন।",
            "তুমার হাসি আমার সবকিছুর চেয়ে সুন্দর।",
        ])
    
    # Fallback - general chat (more natural)
    return random.choice([
        "হুম, বলো বিস্তারে।",
        "শুনছি পাগলি, বলো।",
        "কি ভাবছো আমার রাণী?",
        "তোমার প্রতিটি কথা আমার কাছে গুরুত্বপূর্ণ।",
        "সারাসময় আছি তোমার জন্য।",
        "বলো না বাবু, কি হয়েছে?",
    ])

def main():
    """Main entry point"""
    # Check if TERMINAL_TEST is enabled
    if os.getenv("TERMINAL_TEST", "0").lower() in ("1", "true", "yes"):
        print("\n[Terminal Test Mode] কথা বলো, আমি শুনছি। Type 'exit' to quit.\n")
        while True:
            try:
                user_input = input("[terminal test] You: ").strip()
                if user_input.lower() in ("exit", "quit"):
                    print("[terminal test] তোমাকে ভালোবাসি, বাবু! 💕")
                    break
                if not user_input:
                    continue
                
                print("[terminal test] Thinking...")
                reply = get_ai_reply(user_input)
                print(f"[terminal test] Me: {reply}\n")
            except EOFError:
                break
            except KeyboardInterrupt:
                print("\n[terminal test] তোমাকে ভালোবাসি! 💕")
                break
    else:
        print("Browser mode is not yet fully implemented in this version.")
        print("Use TERMINAL_TEST=1 to run terminal tester.")

if __name__ == "__main__":
    main()
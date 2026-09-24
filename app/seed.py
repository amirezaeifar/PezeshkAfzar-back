from datetime import date


def l(en, fa):
    return {"en": en, "fa": fa}


ARTICLES = [
    {
        "slug": "where-clinical-ai-helps-and-where-it-must-stop",
        "category": "clinicalAI",
        "featured": True,
        "published": True,
        "medical": True,
        "title": l("Where clinical AI helps—and where it must stop", "هوش مصنوعی بالینی کجا کمک می‌کند و کجا باید متوقف شود"),
        "summary": l("A practical way to separate useful decision support from claims a model cannot safely make.", "روشی عملی برای جداکردن پشتیبانی مفید از تصمیم، از ادعاهایی که یک مدل نمی‌تواند با اطمینان مطرح کند."),
        "author": l("Editorial desk", "تحریریه"),
        "reviewer": l("Data and AI governance desk", "گروه راهبری داده و هوش مصنوعی"),
        "datePublished": "2026-09-04",
        "dateModified": "2026-09-14",
        "readingMinutes": 7,
        "image": "/images/home-clinical/journal-care-plan-800.webp",
        "imageWidth": 800,
        "imageHeight": 600,
        "alt": l("A clinician and patient coordinating a care plan beside a laptop", "پزشک و بیمار در حال هماهنگی برنامه مراقبت کنار لپ‌تاپ"),
        "sections": [
            {"id": "start-with-the-decision", "heading": l("Start with the decision, not the model", "از تصمیم شروع کنید، نه از مدل"), "paragraphs": [l("A useful clinical AI project begins by naming the decision, the person responsible for it, and the harm that could follow from a wrong or delayed output. Only then does it make sense to ask what data and model might help.", "یک پروژه مفید هوش مصنوعی بالینی با مشخص‌کردن تصمیم، فرد مسئول آن و آسیبی که ممکن است از خروجی اشتباه یا دیرهنگام ایجاد شود آغاز می‌شود. تازه پس از آن می‌توان پرسید چه داده و مدلی کمک‌کننده است.")], "bullets": []},
            {"id": "define-the-boundary", "heading": l("Write the boundary as carefully as the capability", "مرزها را به اندازه قابلیت‌ها دقیق بنویسید"), "paragraphs": [l("Documentation should explain what the system observes, what it outputs, where it was evaluated, and which conclusions it cannot support.", "مستندات باید روشن کنند سامانه چه چیزی را مشاهده می‌کند، چه خروجی‌ای می‌دهد، کجا ارزیابی شده و از چه نتیجه‌گیری‌هایی پشتیبانی نمی‌کند.")], "bullets": [l("Name the intended user and exact moment of use.", "کاربر هدف و لحظه دقیق استفاده را مشخص کنید."), l("Provide a clear route to disagree and report problems.", "راهی روشن برای مخالفت و گزارش مشکل فراهم کنید.")]},
            {"id": "monitor-after-release", "heading": l("Validation does not end at release", "اعتبارسنجی با انتشار تمام نمی‌شود"), "paragraphs": [l("Clinical populations, workflows, devices, and data pipelines change. Monitoring should look for drift, uneven errors, and workflow side effects.", "جمعیت‌های بالینی، گردش‌کارها، دستگاه‌ها و مسیرهای داده تغییر می‌کنند. پایش باید افت عملکرد، خطاهای نامتوازن و پیامدهای جانبی در جریان کار را بررسی کند.")], "bullets": []},
        ],
        "sources": [
            {"label": l("WHO — Ethics and governance of artificial intelligence for health", "سازمان جهانی بهداشت — اخلاق و راهبری هوش مصنوعی برای سلامت"), "url": "https://www.who.int/publications/i/item/9789240029200"},
            {"label": l("NIST — AI Risk Management Framework", "مؤسسه ملی استانداردها و فناوری — چارچوب مدیریت ریسک هوش مصنوعی"), "url": "https://www.nist.gov/itl/ai-risk-management-framework"},
        ],
    },
    {
        "slug": "human-review-is-part-of-the-system",
        "category": "responsibleAI",
        "featured": False,
        "published": True,
        "medical": True,
        "title": l("Human review is part of the system", "بازبینی انسانی بخشی از خود سامانه است"),
        "summary": l("Human oversight works only when reviewers have context, authority, time, and a way to challenge the machine.", "نظارت انسانی فقط زمانی کار می‌کند که بازبین زمینه، اختیار، زمان و راهی برای به‌چالش‌کشیدن ماشین داشته باشد."),
        "author": l("Editorial desk", "تحریریه"),
        "reviewer": l("Data and AI governance desk", "گروه راهبری داده و هوش مصنوعی"),
        "datePublished": "2026-08-21",
        "dateModified": "2026-09-12",
        "readingMinutes": 6,
        "image": "/images/home-clinical/journal-records-800.webp",
        "imageWidth": 800,
        "imageHeight": 600,
        "alt": l("A medical professional completing patient documentation", "متخصص درمان در حال تکمیل مستندات بیمار"),
        "sections": [
            {"id": "more-than-a-checkbox", "heading": l("Oversight is more than a checkbox", "نظارت انسانی بیشتر از یک تیک ساده است"), "paragraphs": [l("Putting a person after an algorithm does not automatically make a workflow safe. The reviewer needs enough original context and authority to reject an output without friction.", "قرار دادن یک انسان پس از الگوریتم، گردش‌کار را خودبه‌خود ایمن نمی‌کند. بازبین به زمینه اصلی کافی و اختیار لازم برای ردکردن بی‌دردسر خروجی نیاز دارد.")], "bullets": []},
            {"id": "design-the-review-queue", "heading": l("Design the review queue", "صف بازبینی را طراحی کنید"), "paragraphs": [l("A review interface should show why an item entered the queue, what source material supports it, and what happens after each action.", "رابط بازبینی باید نشان دهد چرا یک مورد وارد صف شده، چه محتوای اصلی از آن پشتیبانی می‌کند و پس از هر اقدام چه رخ می‌دهد.")], "bullets": [l("Preserve the unedited source context.", "زمینه و محتوای اصلی ویرایش‌نشده را حفظ کنید."), l("Make uncertainty and missing data obvious.", "عدم‌قطعیت و دادهٔ گمشده را آشکار کنید.")]},
            {"id": "learn-from-disagreement", "heading": l("Treat disagreement as safety data", "اختلاف‌نظر را دادهٔ ایمنی بدانید"), "paragraphs": [l("Patterns of disagreement can reveal ambiguous definitions, missing context, and performance gaps.", "الگوهای اختلاف‌نظر می‌توانند تعریف مبهم، زمینه گمشده و شکاف عملکرد را نشان دهند.")], "bullets": []},
        ],
        "sources": [
            {"label": l("WHO — Ethics and governance of AI for health", "سازمان جهانی بهداشت — اخلاق و راهبری هوش مصنوعی برای سلامت"), "url": "https://www.who.int/publications/i/item/9789240029200"},
            {"label": l("FDA — Transparency for machine learning-enabled medical devices", "سازمان غذا و داروی آمریکا — شفافیت در تجهیزات پزشکی مبتنی بر یادگیری ماشین"), "url": "https://www.fda.gov/medical-devices/software-medical-device-samd/transparency-machine-learning-enabled-medical-devices-guiding-principles"},
        ],
    },
    {
        "slug": "designing-medical-software-around-clinical-workflows",
        "category": "medicalSoftware",
        "featured": False,
        "published": True,
        "medical": True,
        "title": l("Designing medical software around clinical workflows", "طراحی نرم‌افزار پزشکی حول گردش‌کار بالینی"),
        "summary": l("A screen can be efficient while the complete clinical task remains slow, fragmented, or unsafe.", "ممکن است یک صفحه سریع باشد، اما کل کار بالینی همچنان کند، پراکنده یا ناایمن بماند."),
        "author": l("Editorial desk", "تحریریه"),
        "reviewer": l("Clinical review desk", "گروه بازبینی بالینی"),
        "datePublished": "2026-08-08",
        "dateModified": "2026-09-10",
        "readingMinutes": 6,
        "image": "/images/home-clinical/journal-consultation-800.jpg",
        "imageWidth": 800,
        "imageHeight": 600,
        "alt": l("A doctor and patient reviewing a radiograph in a warm consultation room", "پزشک و بیمار در حال بررسی تصویر رادیولوژی در اتاق مشاوره"),
        "sections": [
            {"id": "map-the-whole-task", "heading": l("Map the whole task", "تمام کار را ترسیم کنید"), "paragraphs": [l("Clinical work crosses rooms, roles, devices, and shifts. Research should follow the task from the first signal through documentation, communication, action, and handoff.", "کار بالینی از اتاق‌ها، نقش‌ها، دستگاه‌ها و شیفت‌ها عبور می‌کند. پژوهش باید کار را از نخستین نشانه تا ثبت، ارتباط، اقدام و تحویل دنبال کند.")], "bullets": []},
            {"id": "design-for-interruption", "heading": l("Design for interruption and return", "برای وقفه و بازگشت طراحی کنید"), "paragraphs": [l("A safe interface preserves context, saves progress predictably, and makes unfinished work visible.", "رابط ایمن زمینه را حفظ می‌کند، پیشرفت را قابل‌پیش‌بینی ذخیره می‌کند و کار ناتمام را آشکار نگه می‌دارد.")], "bullets": []},
            {"id": "measure-work-not-clicks", "heading": l("Measure completed work, not isolated clicks", "کار کامل‌شده را بسنجید، نه کلیک‌های جداگانه را"), "paragraphs": [l("Completion time, repeated entry, recovery after interruption, handoff quality, and unresolved work reveal costs that page-level speed misses.", "زمان تکمیل، ثبت تکراری، بازیابی پس از وقفه، کیفیت تحویل و کار حل‌نشده هزینه‌هایی را آشکار می‌کنند که سرعت یک صفحه نمی‌بیند.")], "bullets": []},
        ],
        "sources": [
            {"label": l("ONC — Usability and provider burden", "دفتر هماهنگ‌کننده ملی فناوری اطلاعات سلامت — کاربردپذیری و بار کاری ارائه‌دهنده"), "url": "https://healthit.gov/usability-and-provider-burden/"},
            {"label": l("WHO — Digital health", "سازمان جهانی بهداشت — سلامت دیجیتال"), "url": "https://www.who.int/health-topics/digital-health"},
        ],
    },
]

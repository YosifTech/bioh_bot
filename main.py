from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ضع توكن البوت الجديد هنا بعد تغييره في BotFather
BOT_TOKEN = '7521404607:AAF-Ao-luzVvsq-43Ao6Pe4Ao7QLqqlV-Ho'

# تتبع حالة المستخدم
user_state = {}

# صور الفصول
chapter_images = {
    "الفصل 1": [
        "AgACAgIAAxkBAAIBBGgOVVMeKK722HfIghbyAplDKvq4AAIu9TEbHPdwSJcNibC4MkSCAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBBmgOVaoh_C7FSacv8MTb4EXZHSyCAAI39TEbHPdwSAv7rnxTGwLAAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBCGgOVbZXkYDGNk_9lQwMWxhxlvRbAAIw9TEbHPdwSNqghfrHqDE-AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBCmgOVcZ-6Ky5LQABpZroCvpRofFlMwACLfUxGxz3cEjBJFr4eh_xxQEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAIBDGgOVdar32z88h3tCwgh5I39pXMkAAIx9TEbHPdwSPnMLZrOpe9eAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBDmgOVeR-Y8pRClVuroveAnt-AnRJAAIz9TEbHPdwSPEAAUqWj0N4IAEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAIBEGgOVfJKocAdad7biVawPrXB47bYAAIy9TEbHPdwSHvYZTmB2CWnAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBEmgOVf6w3CJH3m04Y9ngcxrf8Xq3AAI09TEbHPdwSEcFxcqBomHmAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBFGgOVhowl_TPhgW4Krep_nbaDdBdAAI19TEbHPdwSIjuGt1_VoHhAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBFmgOVinxhqhamqBBrkBQzRFxbvEGAAI29TEbHPdwSDFzUCFIu-zxAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBGGgOVjRc3QTBXDABwIi8uBHeCxABAAIv9TEbHPdwSNKINzpCJXhUAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBGmgOVkEQNGy6PsH1XXIUnjnHYeZKAAI69TEbHPdwSBB82xbQifXMAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBHGgOVk6RyQjKk7E-9VkKnPiw0gJWAAI49TEbHPdwSIHQKygIZsEWAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBHmgOVlsH3dZU_vZflxdkptDhq7uyAAI59TEbHPdwSI1cU7Ak_IXHAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBIGgOVmdjIuNSh7VhYzmmaeYWdO3iAAI79TEbHPdwSGefWlDKyUK5AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBImgOVnXd104llAj0dBtjeePqHs9EAAI89TEbHPdwSHGuyjp8UNQeAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIHzWgQ9aJwEQNqSphFPCRPc_rRt-yXAAL78jEbVtOISNUiUO1P5x4AAQEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAIHzmgQ9aI2SZadaQTWUrh9UQmGLlMqAAL68jEbVtOISHjEE0sW-L5dAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIHz2gQ9aIaqNsF35CEO89t0ZpS1tNtAAL88jEbVtOISLbFenA9asOjAQADAgADeQADNgQ"
    ],
    "الفصل 2": [
        "AgACAgIAAxkBAAIBJmgOVxJSfv_CxgFxkkqetZ73-QSdAAIF8zEbqfdxSPAst4wQJvKTAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBKWgOVySyf7bGMr5SM2X0N2ktgZnJAAIK8zEbqfdxSPsD1vFmHj17AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBK2gOVyoPT-33dTGpAAEaQvehwUwTQAACC_MxG6n3cUgX-BX8kIWliAEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAIBLWgOVzZTAruXTFK1NpJXE3iWe2OmAAIM8zEbqfdxSKRKRttXSyfYAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBL2gOV0AlUJkb95W9d_CAzq1ooApvAAIN8zEbqfdxSKLurnLJ1edAAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBMWgOV0iYDplvFttj1bSzmZ1m9JL6AAIO8zEbqfdxSFsgz2ToqChzAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBM2gOV1B1P7-jRBD4RufWd5W-iWTYAAIP8zEbqfdxSHvajpXsNPyhAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH02gQ9quaxjDA0_VtO8-yKA_B1UiuAAIH8zEbVtOISDlxZpaBjGRlAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH1GgQ9qtRPnyYpvc5scE0weC47jHzAAII8zEbVtOISK4IysvGoKvIAQADAgADeQADNgQ"
    ],
    "الفصل 3": [
        "AgACAgIAAxkBAAIBN2gOV4UtHPDXM3rUhJdtk3q_fMu_AAIS8zEbqfdxSFvDoYiK3ASwAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBOGgOV4VgaR_XShqhQGrdiy3V1OmMAAIW8zEbqfdxSMw_90vS9ytAAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBOWgOV4U0p2CubbJS-HC03ZMotgrsAAIZ8zEbqfdxSP6mWyFPUaHaAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBOmgOV4XdQeGDr7LaTyXcuDdrXB6wAAIb8zEbqfdxSLNCz_Amm9jJAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBO2gOV4XA03T3K_MMJO6y3x1FWRHXAAIc8zEbqfdxSBsfYUkVGGdmAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBPGgOV4UGyWFIGOnN3cUVbwK7uEtMAAId8zEbqfdxSHtvKWHg0cg-AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBPWgOV4WOq2xd7YwDvHLqpm0q-NeLAAIU8zEbqfdxSIM-kWo79wb7AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBPmgOV4Uj3kQWpVoNXExR0v2UjzjLAAIe8zEbqfdxSNbFMJ-Z04eyAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBP2gOV4X-9WUIUMMeDQABxpWPHkAebQACH_MxG6n3cUiDEzA_NgkmSgEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAIBQGgOV4WmsI33YLYlXn6RGar88HZeAAIY8zEbqfdxSIokeicGmqC4AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBQWgOV4UdhUIMTFOA5RSn1rhiA1AlAAIT8zEbqfdxSDz8WTRMc5o9AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBQmgOV4WXlrBSzn4SFl65sd3bXCMvAAIV8zEbqfdxSL4kw9IjNiSrAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBQ2gOV4WdQtHpXj0XaM4kVfhG6n8tAAIX8zEbqfdxSKQYw5OM9Ck6AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBRGgOV4VApIThkmbC-OcQJtNbhUWUAAIa8zEbqfdxSJEqsjwk4VZwAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH2WgQ9ubrNyWjZG6Us78KyMBtQycGAAIN8zEbVtOISC98vwyOdYOuAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH2mgQ9uaxPnxC_BWGv9XayUTTIrFFAAIO8zEbVtOISB4D8BIMLypdAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH22gQ9uY9yQcKjJLEH4SnBUvG2W0-AAIM8zEbVtOISDDhK0D2S6q7AQADAgADeQADNgQ"
    ],
    "الفصل 4": [
        "AgACAgIAAxkBAAIBVWgOV-sIWd4244tIV9F8ZXPQfFB2AAKA8zEbqfdxSB3z7ZKJ14ehAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBVmgOV-vTMwWqn01P5BDcsNn7Lt6NAAKC8zEbqfdxSCYbW3wlD_2YAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBV2gOV-uVRSGFTVcsnLLXPl1kyTYWAAKB8zEbqfdxSPXvX7c-LPs_AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBWGgOV-sERfZbGJPInpzR5fEO7oBEAAKD8zEbqfdxSFvwPFyB4kyAAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBWWgOV-up8D7LlZsURDkgm1tiixhuAAKH8zEbqfdxSBIe7W0vwBgDAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBWmgOV-uQWPfVWAEKJYm4R13CMnx3AAKK8zEbqfdxSMk4rDJGj3qIAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBW2gOV-tTsT1jd7sqr3DrX7mIe-xfAAKL8zEbqfdxSIaSc39sTC2pAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBXGgOV-uoaI2GQ0nDbfj483LqObWBAAKN8zEbqfdxSNm9mnSMF1EqAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBXWgOV-vgJjIykdEuWCX79Ihyw9jmAAKO8zEbqfdxSEHWiro0SNBmAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBXmgOV-vFhARfQf-aj2JId2W5zw2lAAKP8zEbqfdxSFpL7DOviIoZAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBX2gOV-stCl_46C0OZjUsnPD82UFKAAKF8zEbqfdxSCTFvCF4iueRAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBYGgOV-sqyxjSaD2bBVZJOZpMFvLLAAKE8zEbqfdxSIs1qxLXtavdAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBYWgOV-si4T3LMr0TnzCb325lVm9-AAKG8zEbqfdxSCsGzo-DmQLJAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBYmgOV-uCZLwhx3lrC6XYbfyamSvUAAKI8zEbqfdxSAABFNK2fSukqAEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAIBY2gOV-vAQfcsQMntcl_wZGw9UVpGAAKJ8zEbqfdxSAtwwPbtL66WAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBZGgOV-vJ-9eMGqpbZIjMGaPJnniEAAKQ8zEbqfdxSPKYB7itqZu6AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBZWgOV-t25Z7WbCWmpZ_6f_-GdHX5AAKM8zEbqfdxSK9FbqqvzI2hAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH32gQ9y5l_OnqjrEbLDrflJ9lY8KwAAIQ8zEbVtOISHgyM-p375kUAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH4GgQ9y5gqeneBUhhdl49yfrdoJmrAAIR8zEbVtOISEN_vHpwHIA4AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH4WgQ9y7pzJCwgRpghi9mp1vJ4NUKAAIS8zEbVtOISBtUgahzLFLwAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH4mgQ9y4iWYxDl-puljP_givxDvUCAAIT8zEbVtOISGYOnxgQJhg-AQADAgADeQADNgQ"
    ],
    "الفصل 5": [
        "AgACAgIAAxkBAAIBeWgOWCBwKgepSyQOCVOr_yrRXZ3gAAIb9DEbqfdxSEXKVoEkSEdXAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBemgOWCBW5ZjGkrFvIJ3YI4QTCvt5AAIe9DEbqfdxSEg0IaV9xWOyAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBe2gOWCAmAnk4S0IzxDo6AwTKqsmHAAIq9DEbqfdxSLc7Uxwhy6vDAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBfGgOWCC-XJL1UXYBfxKFvyK5EiLIAAIg9DEbqfdxSLLivW8xg9HbAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBfWgOWCA3BLn9UGwdntNAabmeXEdmAAIs9DEbqfdxSA577PueIl__AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBfmgOWCBVeZvXaYztj24YeK-TdkRqAAIr9DEbqfdxSIrN3PK5gZ2HAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBf2gOWCAb3DOCsNhAXthjZJj-tds5AAIt9DEbqfdxSKftlmmJ3HrTAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBgGgOWCBQKrGa_7jwmmvfPBK_TE0oAAIv9DEbqfdxSIscAAEUBEvr7QEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAIBgWgOWCD_QacbwTglx67MYcHGC5HiAAIx9DEbqfdxSJV8jNAkTlEGAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBgmgOWCAQ4vDwExX7u7zIT4zTdesdAAI09DEbqfdxSGBkyjt38B0AAQEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAIBg2gOWCAP4WV17lDyCdXKn7S55RYEAAId9DEbqfdxSCyDu0lJpDhRAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBhGgOWCA9CWl-7Yyvz_s6FcMG05fdAAIf9DEbqfdxSM92DCIAATU7JQEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAIH52gQ93V9aQbByN5fs6ybT8ATXJMUAAIW8zEbVtOISAfGAvH9HXxnAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH6GgQ93UQvMEoPyG3O6pyqzKCLOQFAAIX8zEbVtOISK2F0rQXKlKEAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH6WgQ93V8MnzWcil0GUuLXBy49wznAAIV8zEbVtOISCHmL9v2FWKzAQADAgADeQADNgQ"
    ],
    "الفصل 6": [
        "AgACAgIAAxkBAAIBk2gOWFnj4lNRzZvg5KDJbMbBemBeAALO9DEbqfdxSJ72eTn5xF8hAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBlGgOWFnB8hQNDEkIvWOe3LWHcZp2AALR9DEbqfdxSKMnAh3arhHFAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBlWgOWFnGSnYyEL-QRxZ-0-c3tnSUAALQ9DEbqfdxSEmRY8_dx38xAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBlmgOWFnrzELlcvXE7DA0eZ529NVMAALT9DEbqfdxSGTqoIyrLJIOAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBl2gOWFkjTmocWARBxZp4DLybcuyMAALU9DEbqfdxSN__b3gexruSAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBmGgOWFn3iZwZ7twJoLownrTl5MAtAALS9DEbqfdxSPVrUwxcKOdPAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBmWgOWFkquqqfBthhojwntlm82Nw1AALW9DEbqfdxSHJdL_KNztqSAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBmmgOWFm1fwRll04TIdZMsTdqd40gAALV9DEbqfdxSJvwk_CCaoiiAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBm2gOWFlSQJxHa8EGcMDSj7pky00cAALX9DEbqfdxSJDMxnnLiQ13AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBnGgOWFl12R5D8EPvJv2UoYE25bsBAALP9DEbqfdxSFTii33pKivmAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH7WgQ97ezrMZdAl6b3Vpvb30Rws-vAAIa8zEbVtOISEYQyZ13M45MAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH7mgQ97c5Kr0ZaQJshQsbCWm8Q47sAAIZ8zEbVtOISOCVUvsnCFusAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH72gQ97e7VcYuZ4-CCC1p8W8tLl7rAAIb8zEbVtOISKZrLBUBQR0UAQADAgADeQADNgQ"
    ],
    "الفصل 7": [
        "AgACAgIAAxkBAAIBqWgOWItKmzvE5QwO5psHeEsrnsiwAAJN9TEbqfdxSPntPG6_Z4VCAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBqmgOWIs9ySnhdtSqPiRzg_EdL66VAAJO9TEbqfdxSLl8FAuZYQjxAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBq2gOWIu64bl1f_J8yYnnYBr3MkOhAAJQ9TEbqfdxSJdL8-aRUcPzAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBrGgOWIuFTj6jdC1HKecQa8BKp6ohAAJS9TEbqfdxSPbN6v0lpksUAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBrWgOWIsijcwhYQmw9W69ltKYYmNhAAJP9TEbqfdxSCyIfPHGGbkTAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBrmgOWItSCrg7PXU00GcSdrC3sGElAAJR9TEbqfdxSMT_dI432iJHAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBr2gOWIvoYFH5TkXe9sRtY6ukPmIbAAJT9TEbqfdxSF7ao700WPrcAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH82gQ9-V7W1PF1Z_eF3Qu1YZji2gLAAIh8zEbVtOISB76xmX4zfhNAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH9GgQ9-XWvKyRF0Sz2qEHT8twcRyNAAIj8zEbVtOISFMtfbVMQ2c0AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH9WgQ9-Wxsw6Ciwasff0HK4-Bf1x6AAIi8zEbVtOISNMTppPgcbnmAQADAgADeQADNgQ"
    ],
    "الفصل 8": [
        "AgACAgIAAxkBAAIBuWgOWK8wECAO16KcVlIe7axR2qIcAAJW9TEbqfdxSDaYaFIfO4EKAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBumgOWK_RXfuRXoJm5AnVytzIR6uZAAJY9TEbqfdxSAgEF2V2SUHKAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBu2gOWK9lRo4nO1kpxOk79VeupZJNAAJa9TEbqfdxSJCaH-svwTszAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBvGgOWK-8KIzAmhmCp18pUaLDzfGAAAJX9TEbqfdxSKmsLKpuP814AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBvWgOWK_DYA5oR9X4EoNGeG-2avtlAAJb9TEbqfdxSIFSdpnqdqKhAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBvmgOWK9fIJ3GDm_3y5MqtbMcgTDvAAJZ9TEbqfdxSLhw7zdZgFYfAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH-WgQ-A8hChsl6Ac9jc9ClNOHaPSIAAIk8zEbVtOISG2oZpOXZZ3FAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH-mgQ-A8_LPyXM9A3tfddMvyqlso_AAIl8zEbVtOISNfV8kV_kNq8AQADAgADeQADNgQ"
    ],
    "الفصل 9": [
        "AgACAgIAAxkBAAIBx2gOWNNkXcVQIaLCFZ03wNSXVFLFAAJc9TEbqfdxSNNQoYYRcwadAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIByGgOWNNTZq2N_vYTulmTythUtd7AAAJd9TEbqfdxSD4hoS2eb1MJAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIByWgOWNMUGwZrysQaN9YLERKgNxfUAAJe9TEbqfdxSIMUth5iJcyDAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBymgOWNOzks-h_I2h9mv2O-U4fppkAAJf9TEbqfdxSGBj5-SD_KsSAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBy2gOWNOp1WTvuw0Ea9AlRPYgNzMcAAJg9TEbqfdxSOo2JQUPAAGIuAEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAIBzGgOWNOC1Iyeu1e2Of-juNhUbMGBAAJh9TEbqfdxSCFmDeU6GB59AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBzWgOWNO2LriYWBablS00RCec6NJ6AAJi9TEbqfdxSDtPOLtOhIOEAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBzmgOWNMFQlxOsoZdkUn1YqDNfmz7AAJj9TEbqfdxSGz4dxd4qrjRAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIBz2gOWNNR8T4Wi6sNDLYhc3_AGhleAAJk9TEbqfdxSGQZFlpo55PKAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIB0GgOWNOGPiLDnJDEkCvvCyg3_UZtAAJl9TEbqfdxSM5ykn3hmfsUAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIB0WgOWNNdAAGtlHaj67vePFt83gJ2hAACZvUxG6n3cUgXhWbgIHqt0AEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAIH_WgQ-D5zLCtoamWSXzpsuZ8hn3eJAAIm8zEbVtOISNAESf1RCaMMAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH_mgQ-D7vblHF-zpbFJeOBKu_3G2-AAIn8zEbVtOISKrB4IkHQ2ikAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIH_2gQ-D5xm8IXngy5AAFEn8V2zvgrXwACKPMxG1bTiEgtFIWy9EjltwEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAIIAAFoEPg-snKMawZ0s2NuoAFMVEonlQACKfMxG1bTiEhah08LzM1veAEAAwIAA3kAAzYE"
    ],
    "الفصل 10": [
        "AgACAgIAAxkBAAIB32gOWQSgqG3BO2aPMDBmEb2qqCy3AAJn9TEbqfdxSEXHaj4-VNzRAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIB4GgOWQRXVJxce2exsrmmgk_BNngNAAJo9TEbqfdxSFH5zFPaxZ_9AQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIB4WgOWQSaR0oOl_pjK2SErgABm29KGQACafUxG6n3cUgtjgcif7wmgQEAAwIAA3kAAzYE",
        "AgACAgIAAxkBAAIB4mgOWQTQVHVUbUUOLqj9Bo7iA01wAAJq9TEbqfdxSKpy4hf_O03eAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIB42gOWQTfQ_iLohoFa1bincgXUuDfAAJr9TEbqfdxSDXP_SkKFF7VAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIIBWgQ-GvEsjKHD8wWljUGzk30v5lCAAIs8zEbVtOISPZAPwhUy0xVAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIIBmgQ-GtcK2mc7G-OQ9WoRGbm6ItlAAIt8zEbVtOISOv7I9iVE_1YAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIIB2gQ-Gt0Ra_ZhQUgHAXIxw9pXqNnAAIr8zEbVtOISAbKj8Ad8dN6AQADAgADeQADNgQ"
    ],
    "الفصل 11": [
        "AgACAgIAAxkBAAIB62gOWSvIqUnVb7bparNkZnK6UIPlAAJw9TEbqfdxSCGvXPbZ2K8MAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIB7GgOWStACMG61yuKB6sy0F6H9n6XAAJy9TEbqfdxSDDuVVUEXQ6hAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIB7WgOWSvlWjTtUEttCik_3KSMTxd5AAJx9TEbqfdxSNukipW6kmnyAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIB7mgOWSsRJnNhlcyYbsSq1SkKsgkcAAJz9TEbqfdxSNoMy7qpXlbfAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIB72gOWSuMyjmtfH_rr1NFzaZNInVEAAJ09TEbqfdxSFfFhbI1ZepbAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIIC2gQ-JyeI7kwkzPLATZXeca2XTYEAAIx8zEbVtOISIBF5P1VmKixAQADAgADeQADNgQ",
        "AgACAgIAAxkBAAIIDGgQ-JxCM2twKXFE-zWSz79ivea2AAIy8zEbVtOISKKp8b977SnWAQADAgADeQADNgQ"
    ]

}

# أسئلة وزارية
third_ques_images = [
 
    "AgACAgIAAxkBAAIFWmgPwqoMNMvDmTQVJFmNJPKAPLGbAAL56DEbqfeBSD7Y_oR8-PRMAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIFW2gPwqqdvPjcN47UDvrT_HGY3JHoAAL66DEbqfeBSMfmlOr-1frvAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIFXGgPwqryVtfDUBOQ1sf4a0i6xxmbAAL96DEbqfeBSPq7026K1GEDAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIFXWgPwqptF3VDmNuw-YpDrcoRCsozAAL76DEbqfeBSBN77xpmoQNgAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIFXmgPwqq18PfjID6NSx-euvP_DtIVAAL_6DEbqfeBSAG2HB0FTqC-AQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIFX2gPwqrKz_myS5rH3iRcmHDyqBtBAAL-6DEbqfeBSKvmxe7N9ARFAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIFYGgPwqr_SMnH8YcY0o_YdIWsM8PcAAPpMRup94FIhtT6quFYzowBAAMCAAN5AAM2BA",
    "AgACAgIAAxkBAAIFYWgPwqoitv94ti1TJKj7tGXywtfpAAIB6TEbqfeBSKKl36r5lsqnAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIFYmgPwqrmvaPYQkmUskXp3cBrL7_ZAAIG6TEbqfeBSBCTruaBRgffAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIFY2gPwqrdu1tf6_x4HNR3Qp4w_JmrAAIC6TEbqfeBSKXCsD_3uGDcAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIFZGgPwqqXLQphgutw6ZTMyC0gjzusAAIJ6TEbqfeBSGU-TlGvm_hSAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIFZWgPwqraHqlSoAYiXvi8xWIK27enAAIH6TEbqfeBSAjlbB5xgNaJAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIFZmgPwqqJQtDQkLN-kpopcYufMrePAAII6TEbqfeBSCaVXqX3iFuVAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIFZ2gPwqp3KeV2_9ssaWIzdGdIMkbMAAID6TEbqfeBSMfl0Gdlt0mpAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIFaGgPwqpp5eVBY2x2gfU4kGslgR9rAAIK6TEbqfeBSAYrJHWa2Wj7AQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIFaWgPwqoPlU_TqiJOxp0tpAt2BnHEAAIE6TEbqfeBSIqxDVw-1kudAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIFamgPwqoGpIxr5U8OFtNOKV9PGhTzAAL86DEbqfeBSPEWhj41OzALAQADAgADeQADNgQ",
    "AgACAgIAAxkBAAIFa2gPwqpTF-v5J91CUxGumm997obiAAIF6TEbqfeBSIOqAyW97baWAQADAgADeQADNgQ"

]

# نقاط توفر الملزمة مع تسميات الأزرار الجديدة
sales_points = {
       "النجف : مكتبة البغدادي": (
        "مكتبة البغدادي: النجف شارع الجامعة مقابل مدارس بانيقيا الأهلية.\n"
        "**للحجز المسبق:** 07801306615\n@ssoon1234"
    ),
    "بغداد : مكتبة القلعة": (
        "مكتبة القلعة: بغداد حي الخضراء مقابل ثانوية المتميزين.\n"
        "**للحجز المسبق:** 07728662032\n@sino89"
    ),
    "الموصل : مكتبة الشمس": (
        "الموصل المجموعة الثقافية مقابل نفق الجامعة\n"
        "**للحجز المسبق:** 07704141808\n@alshames123"
    ),
    "ديالى المقدادية : مكتبة الرحمن": (
        "ديالى المقدادية الوجيهية قرب اعدادية الوجيهية\n"
        "**للحجز المسبق:** 07726222219\n@nbras2010"
    ),
    "ديالى الخالص : مكتبة الزهراء": (
        "ديالى الخالص السوق شارع الأطباء خلف المصرف.\n"
        "**للحجز المسبق:** 07707867592\n@Wasamskee"
    ),
    "الموزع الرئيسي": (
        "**للحجز المسبق:\n** 07707969053\n@aawraaq"
    )

}

async def send_media_grouped(update: Update, context: ContextTypes.DEFAULT_TYPE, images: list):
    """
    يجزئ الصور إلى مجموعات من 10 ويستخدم send_media_group لإرسال كل مجموعة كألبوم
    """
    chunk_size = 10
    chat_id = update.effective_chat.id
    for i in range(0, len(images), chunk_size):
        chunk = images[i:i + chunk_size]
        media = [InputMediaPhoto(media=file_id) for file_id in chunk]
        await context.bot.send_media_group(chat_id=chat_id, media=media)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["الثالث المتوسط", "السادس العلمي"]]
    await update.message.reply_text(
        "اختر المرحلة:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    user_state[update.effective_user.id] = "start"

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    # خيار المرحلة الثالثة
    if text == "الثالث المتوسط":
        keyboard = [
            ["المادة العلمية 📚", "الاسئلة الوزارية 📝"],
            ["الاستفسارات 💬", "نقاط توفر الملزمة 🛒"],
            ["رجوع ↩"]
        ]
        await update.message.reply_text("اختر:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        user_state[user_id] = "third_options"
        return

    # خيار المرحلة السادسة العلمية
    if text == "السادس العلمي":
        await update.message.reply_text("قريبًا.. الصفحة قيد الإنشاء 🔜")
        return

    # عرض الأسئلة الوزارية
    if text == "الاسئلة الوزارية 📝":
        await send_media_grouped(update, context, third_ques_images)
        return

    # عرض فصول المادة العلمية
    if text == "المادة العلمية 📚":
        keyboard = [[f"الفصل {i}"] for i in range(1, 12)] + [["رجوع ↩"]]
        await update.message.reply_text("اختر الفصل:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        user_state[user_id] = "material"
        return

    # عرض صور الفصل المختار
    if text in chapter_images:
        await send_media_grouped(update, context, chapter_images[text])
        return

    # عرض نقاط البيع
    if text == "نقاط توفر الملزمة 🛒":
        keyboard = [[btn] for btn in sales_points.keys()] + [["رجوع ↩"]]
        await update.message.reply_text(
            "اختر نقطة البيع:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        user_state[user_id] = "sales_options"
        return

    # عند اختيار نقطة بيع
    if user_state.get(user_id) == "sales_options" and text in sales_points:
        await update.message.reply_text(sales_points[text], parse_mode="Markdown")
        keyboard = [[btn] for btn in sales_points.keys()] + [["رجوع ↩"]]
    
        return

    # زر رجوع
    if text == "رجوع ↩":
        prev = user_state.get(user_id)
        if prev == "sales_options":
            keyboard = [
                ["المادة العلمية 📚", "الاسئلة الوزارية 📝"],
                ["الاستفسارات 💬", "نقاط توفر الملزمة 🛒"],
                ["رجوع ↩"]
            ]
            await update.message.reply_text("اختر:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
            user_state[user_id] = "third_options"
            return
        if prev == "third_options":
            keyboard = [["الثالث المتوسط", "السادس العلمي"]]
            await update.message.reply_text(
                "يرجى تحديد المرحلة:",
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            )
            user_state[user_id] = "start"
            return
        if prev == "material":
            keyboard = [
                ["المادة العلمية 📚", "الاسئلة الوزارية 📝"],
                ["الاستفسارات 💬", "نقاط توفر الملزمة 🛒"],
                ["رجوع ↩"]
            ]
            await update.message.reply_text("اختر:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
            user_state[user_id] = "third_options"
            return

    # خيار الاستفسارات
    if text == "الاستفسارات 💬":
        await update.message.reply_text(
            "السلام عليكم..\n"
            "يرجى كتابة *أسئلتكم أو استفساراتكم العلمية*.. وسيتم الرد في أقرب وقت.",
            parse_mode="Markdown"
        )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    print("Bot is running...")
    app.run_polling()


if __name__ == '__main__':
    main()

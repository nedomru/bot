import logging

from aiogram import Router, F, Bot, types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

inline_router = Router()

# Локальный список MnA
MNA_DATA = [
    {
        "name": "Interzet",
        "authorization": "IPoE Static",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3289"
    },
    {
        "name": "Акадо (СПБ)",
        "authorization": "DHCP mac+vlan",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3291"
    },
    {
        "name": "Инфоцентр (Сосновый бор)",
        "authorization": "IPoE Static",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3285"
    },
    {
        "name": "Конвекс/ТКС (ЕКБ)",
        "authorization": "IPoE Static / PPTP (общежития)",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/2769"
    },
    {
        "name": "Westcall (СПб)",
        "authorization": "DHCP mac+vlan",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3286"
    },
    {
        "name": "Кредолинк (СПб)",
        "authorization": "DHCP mac+vlan",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3283"
    },
    {
        "name": "MSNet (СПБ)",
        "authorization": "DHCP mac+vlan",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3287"
    },
    {
        "name": "С-Телеком МСК (Самолет)",
        "authorization": "DHCP / PPPoE",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/3238"
    },
    {
        "name": "Дианэт (Барнаул и область)",
        "authorization": "PPPoE / L2TP",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/folder/582/article/2646"
    },
    {
        "name": "НТС (Томск)",
        "authorization": "IPoE DHCP",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/article/3648"
    },
    {
        "name": "Кроникс/Rinet",
        "authorization": "DHCP / DHCP mac+vlan",
        "connection": "Ethernet",
        "link": "https://clever.ertelecom.ru/content/space/4/article/3246/page/3"
    }
]

ROUTER_DATA = [
{
          "name": "TP-Link Зеленка",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Green_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Green_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Green_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Green_010",
          "settings": "0.1/tplinkwifi.net",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2312?text=Зеленый+Settings",
          "emulator": [
            "https://www.tp-link.com/resources/simulator/TL-WR1045ND(RU)_2.0/Index.htm",
          ],
        },
        {
          "name": "TP-Link Archer С5/С9/EC220",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Turquoise_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Turquoise_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Turquoise_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Turquoise_014",
          "settings": "0.1/tplinkwifi.net",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2312?text=TP-Link+Archer+С5,+С9,+EC220",
          "emulator":
            "https://emulator.tp-link.com/Archer_C5(RUS)v4_Router_Emulator/web/index.htm",
        },
        {
          "name": "TP-Link Archer C20/C2/A5/C50/AC750",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Turquoise_v2_C20_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Turquoise_v2_C20_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Turquoise_v2_C20_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Turquoise_v2_C20_010",
          "settings": "0.1/tplinkwifi.net",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2312?text=Archer+C20,+C2,+A5,+C50,+AC750",
          "emulator":
            "https://emulator.tp-link.com/Emulator_ArcherC20_RU_v4/index.htm",
        },
        {
          "name": "TP-Link Archer A6/C7/C60/A9",
          "pppoe":
            "https://clever.ertelecom.ru/content/space/4/folder/465/article/12817/page/0#tp_link_a_osn_pppoe",
          "dhcp": "https://clever.ertelecom.ru/content/space/4/folder/465/article/12817/page/0#tp_link_a_osn_dhcp",
          "ipoe": "https://clever.ertelecom.ru/content/space/4/folder/465/article/12817/page/0#tp_link_a_osn_static",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Turquoise_v2_C20_010",
          "settings": "0.1/tplinkwifi.net",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2312?text=TP-Link+Archer+A6,+C7,+C60,+A9",
          "emulator": "https://emulator.tp-link.com/c7v5_ru/index.html",
        },
        {
          "name": "TP-Link Archer C80",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Turquoise_C80_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Turquoise_C80_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Turquoise_C80_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Turquoise_C80_009",
          "settings": "0.1/tplinkwifi.net",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2312?text=Archer+C80",
          "emulator":
            "https://emulator.tp-link.com/c80-ru-router/index.html#networkMap",
        },
        {
          "name": "TP-Link Archer АХ20/C54",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Turquoise_AX20_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Turquoise_AX20_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Turquoise_AX20_004",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TPLink_Turquoise_AX20_009",
          "settings": "0.1/tplinkwifi.net",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2312?text=Archer+АХ20+/+Archer+C54",
          "emulator":
            "https://emulator.tp-link.com/Archer_AX90v1_EU_simulator/index.html#tpLinkCloud",
        },
        {
          "name": "D-Link DIR-300NRU/DIR-615 Темная",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_Grey_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_Grey_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_Grey_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_Grey_009",
          "settings": "0.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2275?text=DIR-300NRU+/+DIR-615",
          "emulator": "http://em.dlink.ru/emul/DIR-300AD_gray/",
        },
        {
          "name": "D-Link DIR-300/DIR-615 Желтая",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_Grey-orange_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_Grey-orange_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_Grey-orange_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_Grey-orange_009",
          "settings": "0.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2275?text=D-Link+DIR-300+/+DIR-615",
          "emulator": "http://linserv.ru/dlink-DIR-615/",
        },
        {
          "name": "D-Link DIR-615 Белая",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_White_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_White_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_White_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_White_009",
          "settings": "0.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2275?text=DIR-615",
          "emulator": "http://em.dlink.ru/emul/DIR-615KR1/#start/storInfo",
        },
        {
          "name": "D-Link DIR-300NRU/DIR-620",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_White-turquoise_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_White-turquoise_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_White-turquoise_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_White-turquoise_009",
          "settings": "0.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2275?text=DIR-300NRU+/+DIR-620",
          "emulator": "Нет",
        },
        {
          "name": "D-Link DIR300NRU B5/DIR320NRU/DIR-620",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_White-blue_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_White-blue_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_White-blue_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_White-blue_009",
          "settings": "0.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2275?text=DIR300NRU+B5+/+DIR320NRU+/+DIR-620",
          "emulator": "Нет",
        },
        {
          "name": "D-Link DIR-2150/DIR-825/DIR-X1530/DIR-842",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_V3_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_V3_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_V3_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__DLink_V3_009",
          "settings": "0.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2275?text=DIR+2150+/+DIR+825+/+DIR-X1530",
          "emulator": "https://anweb.dlink.ru",
        },
        {
          "name": "Keenetic Lite II-III/Lite NDMS 2.0",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Keenetic_Dark-blue_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Keenetic_Dark-blue_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Keenetic_Dark-blue_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Keenetic_Dark-blue_009",
          "settings": "1.1/my.keenetic.net",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2510?text=Keenetic+Lite+II-III+/+Lite+NDMS+2.0",
          "emulator": "http://routers.nvbs.ru/zyxel/NDMSv2_by_Anna/status.html",
        },
        {
          "name": "Keenetic Lite/ZyXel NBG334W EE",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Keenetic_Blue_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Keenetic_Blue_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Keenetic_Blue_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Keenetic_Blue_009",
          "settings": "1.1/my.keenetic.net",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2510?text=Keenetic+Lite+/+ZyXel+NBG334W EE",
          "emulator":
            "https://itel.ua/emulations/zyxel_keenetic_giga/default.htm",
        },
        {
          "name": "Keenetic Ultra/Giga/Viva/Speedster",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Keenetic_Giga_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Keenetic_Giga_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Keenetic_Giga_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Keenetic_Giga_010",
          "settings": "1.1/my.keenetic.net",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2510?text=Keenetic+Ultra/Giga/Viva/+Speedster",
          "emulator": "https://giga.demo.keenetic.pro/dashboard",
        },
        {
          "name": "Keenetic AlR/Zyxel VIVA/Zyxel CITY/Zyxel START",
          "pppoe":
            "Нет",
          "dhcp": "Нет",
          "ipoe": "Нет",
          "channels": "Нет",
          "settings": "1.1/my.keenetic.net",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2510?text=Zyxel+AlR+/+Zyxel+VIVA+/+Zyxel+CITY+/+Zyxel+START",
          "emulator": "https://giga.demo.keenetic.pro/dashboard",
        },
        {
          "name": "Xiaomi Белая",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Xiaomi_Mi-Router3_004",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Xiaomi_Mi-Router3_005",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Xiaomi_Mi-Router3_006",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Xiaomi_Mi-Router3_009",
          "settings": "31.1/miwifi.com/router.miwifi.com",
          "bz": "https://clever.ertelecom.ru/content/space/4/bookmark/34/article/2509?text=Xiaomi+Mi+Wi-Fi+Router+3",
          "emulator": "http://linserv.ru/Xiaomi/cgi-bin/luci/home",
        },
        {
          "name": "Xiaomi Черная",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Xiaomi_Mi-Router_004",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Xiaomi_Mi-Router_005",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Xiaomi_Mi-Router_006",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Xiaomi_Mi-Router_008",
          "settings": "31.1/miwifi.com/router.miwifi.com",
          "bz": "https://clever.ertelecom.ru/content/space/4/bookmark/34/article/2509?text=Xiaomi+Mi+Wi-Fi+Router",
          "emulator": "Нет",
        },
        {
          "name": "ASUS RT-AC66U/RT-N66U/RT-N65U Темная",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__ASUS_RT_6xxx_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__ASUS_RT_6xxx_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__ASUS_RT_6xxx_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__ASUS_RT_6xxx_011",
          "settings": "1.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/bookmark/34/article/2520?text=ASUS+RT-AC66U+/+RT-N66U+/+RT-N65U",
          "emulator": "https://demoui.asus.com/",
        },
        {
          "name": "ASUS RT-N10/RT-G32/RT32G Голубая",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__ASUS_RT_3xxx_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__ASUS_RT_3xxx_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__ASUS_RT_3xxx_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__ASUS_RT_3xxx_011",
          "settings": "1.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/bookmark/34/article/2520?text=ASUS+RT-N10+/+RT-G32+/+RT32G",
          "emulator": "https://routers.wtf/emul/ASUS1%20OFFLINE/index.html",
        },
        {
          "name": "ASUS WL-520GC Розовая",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__ASUS_WL_5xxx__003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__ASUS_WL_5xxx__004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__ASUS_WL_5xxx__004",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__ASUS_WL_5xxx__010",
          "settings": "1.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/bookmark/34/article/2520?text=ASUS+WL-520GC",
          "emulator":
            "https://routers.wtf/emul/ASUS%20VIOLET%20OFFLINE/index-2.html",
        },
        {
          "name": "Rotek",
          "pppoe":
            "https://clever.ertelecom.ru/content/space/4/bookmark/34/article/8178?fileView=47495",
          "dhcp": "https://clever.ertelecom.ru/content/space/4/bookmark/34/article/8178?fileView=47494",
          "ipoe": "https://clever.ertelecom.ru/content/space/4/bookmark/34/article/8178?fileView=47492",
          "channels": "Нет",
          "settings": "0.1/user/connect5.html",
          "bz": "https://clever.ertelecom.ru/content/space/4/bookmark/34/article/8178?text=Rotek+RX22301/22200",
          "emulator": "Нет",
        },
        {
          "name": "Mercusys",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Mercusys_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Mercusys_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Mercusys_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Mercusys_007",
          "settings": "1.1/mwlogin.net",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2076?text=Mercusys",
          "emulator": "https://www.mercusys.com/ru/support/simulator",
        },
        {
          "name": "Huawei HG231F",
          "pppoe":
            "https://clever.ertelecom.ru/content/space/4/folder/631/article/8179?fileView=47530",
          "dhcp": "Нет",
          "ipoe": "Нет",
          "channels": "Нет",
          "settings": "3.1/1.100",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/8179?text=Huawei+HG231F",
          "emulator": "Нет",
        },
        {
          "name": "Huawei WS880",
          "pppoe":
            "https://clever.ertelecom.ru/content/space/4/folder/631/article/8179?fileView=47539",
          "dhcp": "Нет",
          "ipoe": "Нет",
          "channels": "Нет",
          "settings": "3.1/1.100",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/8179?text=Huawei+ws880",
          "emulator": "Нет",
        },
        {
          "name": "Huawei HG532e",
          "pppoe":
            "https://clever.ertelecom.ru/content/space/4/folder/631/article/8179?fileView=47549",
          "dhcp": "Нет",
          "ipoe": "Нет",
          "channels": "Нет",
          "settings": "3.1/1.100",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/8179?text=Huawei+HG532e",
          "emulator": "Нет",
        },
        {
          "name": "Huawei AX(2,3)",
          "pppoe":
            "https://clever.ertelecom.ru/content/space/4/folder/631/article/8179?fileView=47560",
          "dhcp": "https://clever.ertelecom.ru/content/space/4/folder/631/article/8179?fileView=47562",
          "ipoe": "https://clever.ertelecom.ru/content/space/4/folder/631/article/8179?fileView=47561",
          "channels": "Нет",
          "settings": "3.1/1.100",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/8179?text=Huawei+AX3",
          "emulator": "Нет",
        },
        {
          "name": "SNR-CPE-W4N",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__SNR-CPE-W4N_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__SNR-CPE-W4N_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__SNR-CPE-W4N_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__SNR-CPE-W4N_009",
          "settings": "1.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2515?text=SNR-CPE-W4N",
          "emulator": "http://linserv.ru/SNR-CPE-W4n/home.html",
        },
        {
          "name": "SNR-CPE-W4N ревизия M",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__SNR-CPE-W4N-revM_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__SNR-CPE-W4N-revM_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__SNR-CPE-W4N-revM_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__SNR-CPE-W4N-revM_009",
          "settings": "1.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2515?text=SNR-CPE-W4N+ревизия+M",
          "emulator": "http://linserv.ru/SNR-CPE-W4n/home.html",
        },
        {
          "name": "Tenda new AC/F300",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Tenda_AC_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Tenda_AC_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Tenda_AC_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Tenda_AC_008",
          "settings": "0.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2598?text=Tenda+New+AC+/+F300",
          "emulator": "http://simulator.tendacn.com/F300v2/",
        },
        {
          "name": "Tenda W303R/W309R/W316R",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Tenda_W303R_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Tenda_W303R_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Tenda_W303R_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Tenda_W303R_008",
          "settings": "0.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2598?text=Tenda+W303R/W309R/W316R",
          "emulator": "Нет",
        },
        {
          "name": "Tenda W311R",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Tenda_W311R_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Tenda_W311R_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Tenda_W311R_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Tenda_W311R_008",
          "settings": "0.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2598?text=Tenda+W311R",
          "emulator": "Нет",
        },
        {
          "name": "Tenda F300",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Tenda_F300_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Tenda_F300_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Tenda_F300_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Tenda_F300_008",
          "settings": "0.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2598?text=Tenda+F300",
          "emulator": "http://simulator.tendacn.com/F300v2/",
        },
        {
          "name": "Tenda new",
          "pppoe":
            "https://clever.ertelecom.ru/content/space/4/folder/465/article/13777",
          "dhcp": "https://clever.ertelecom.ru/content/space/4/folder/465/article/13778",
          "ipoe": "https://clever.ertelecom.ru/content/space/4/folder/465/article/13779",
          "channels": "Нет",
          "settings": "0.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/folder/631/article/2598?text=Tenda+new",
          "emulator": "http://simulator.tendacn.com/F300v2/",
        },
        {
          "name": "MikroTik",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Mikrotik_hAP-Lite-TC_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Mikrotik_hAP-Lite-TC_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Mikrotik_hAP-Lite-TC_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Mikrotik_011",
          "settings": "88.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2082?text=MikroTik+hAP+Lite+TC",
          "emulator": "https://demo.mt.lv/webfig/#System:Password.Change_Now",
        },
        {
          "name": "NetGear WNR3500L (серый)",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__NetGear_Grey_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__NetGear_Grey_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__NetGear_Grey_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__NetGear_Grey_009",
          "settings": "1.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2507?text=NetGear+WNR3500L+(серый)",
          "emulator": "http://routeremulator.com/netgear_genie/start.html",
        },
        {
          "name": "NetGear (синий)",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__NetGear_Blue_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__NetGear_Blue_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__NetGear_Blue_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__NetGear_Blue_009",
          "settings": "1.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2507?text=NetGear+(синий)",
          "emulator": "http://routeremulator.com/netgear_genie/start.html",
        },
        {
          "name": "Netgear EVG-1500 (Дом.ru)",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__NetgearDomru_003",
          "dhcp": "Нет",
          "ipoe": "Нет",
          "channels": "Нет",
          "settings": "1.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2507?text=Netgear+EVG-1500+(Дом.ru)",
          "emulator": "Нет",
        },
        {
          "name": "Sagemcom f@st 2804 v7",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Sagemcom_003",
          "dhcp": "Нет",
          "ipoe": "Нет",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Sagemcom_006",
          "settings": "1.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2513?text=Sagemcom+f@st+2804+v7",
          "emulator": "http://linserv.ru/FAST-2804v7/",
        },
        {
          "name": "Linksys Smart Wi-Fi",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Linksys_SmartWiFi_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Linksys_SmartWiFi_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Linksys_SmartWiFi_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Linksys_SmartWiFi_007",
          "settings": "1.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2080?text=Linksys+Smart+Wi-Fi",
          "emulator":
            "https://ui.linksys.com/SmartWi-FiFamilyRouters/WRT1200AC/1.0.99.166464/",
        },
        {
          "name": "Linksys e1200",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Linksys_E1200_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Linksys_E1200_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Linksys_E1200_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Linksys_E1200_008",
          "settings": "1.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2080?text=Linksys+e1200",
          "emulator": "https://ui.linksys.com/ExpertFamily/E1200/2.0.04",
        },
        {
          "name": "Netis Белый",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Netis_White_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Netis_White_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Netis_White_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Netis_White_009",
          "settings": "1.1/netis.cc",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2078?text=Netis+(Белый+Settings)",
          "emulator":
            "https://www.netisru.com/Uploads/Support/Emulators/WF2780_EN/index.htm",
        },
        {
          "name": "Netis Синий",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Netis_Blue_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Netis_Blue_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Netis_Blue_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Netis_Blue_008",
          "settings": "1.1/netis.cc",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2078?text=Netis+(Синий+Settings)",
          "emulator": "http://linserv.ru/Netis-WF2501/",
        },
        {
          "name": "Apple AirPort",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router_AirPort_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router_AirPort_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router_AirPort_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router_AirPort_007",
          "settings": "Нет",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2069?text=Настройка+роутеров",
          "emulator": "Нет",
        },
        {
          "name": "Honor",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Honor_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Honor_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Honor_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Honor_007",
          "settings": "3.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2075?text=Настройка+роутеров",
          "emulator": "Нет",
        },
        {
          "name": "Totolink",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Totolink_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Totolink_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Totolink_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Totolink_008",
          "settings": "1.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2084?text=Настройка+роутеров",
          "emulator":
            "https://www.totolink.net/data/popwin/web/A5004NS.9.38/index.htm",
        },
        {
          "name": "TRENDnet TEW-652BRP",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TRENDnet_TEW-652BRP_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TRENDnet_TEW-652BRP_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TRENDnet_TEW-652BRP_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TRENDnet_TEW-652BRP_007",
          "settings": "10.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2081?text=TRENDnet+TEW-652BRP",
          "emulator":
            "https://www.trendnet.com/emulators/TEW-652BRP_V3.2R/wireless_basic.htm",
        },
        {
          "name": "TRENDnet New (TEW-827DRU)",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TRENDnet_TEW-827DRU_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TRENDnet_TEW-827DRU_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TRENDnet_TEW-827DRU_004",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__TRENDnet_TEW-827DRU_007",
          "settings": "10.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2081?text=TRENDnet+New+(TEW-827DRU)",
          "emulator":
            "https://www.trendnet.com/emulators/TEW-827DRU_v2.0R/adm_status.html",
        },
        {
          "name": "Upvel UR-354AN4G",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Upvel_UR-354AN4G_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Upvel_UR-354AN4G_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Upvel_UR-354AN4G_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Upvel_UR-354AN4G_007",
          "settings": "10.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2521?text=Upvel+UR-354AN4G",
          "emulator": "http://linserv.ru/Upvel-UR-314AWN/",
        },
        {
          "name": "Upvel UR-315BN",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Upvel_UR-315BN_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Upvel_UR-315BN_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Upvel_UR-315BN_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Upvel_UR-315BN_008",
          "settings": "10.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2521?text=Upvel+UR-315BN",
          "emulator": "Нет",
        },
        {
          "name": "Upvel UR-325BN/UR-322N4G",
          "pppoe":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Upvel_UR-325BN_003",
          "dhcp": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Upvel_UR-325BN_004",
          "ipoe": "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Upvel_UR-325BN_005",
          "channels":
            "https://dom.ru/faq/instruktsii-po-oborudovaniyu/router__Upvel_UR-325BN_008",
          "settings": "10.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2521?text=Upvel+UR-325BN+/+UR-322N4G",
          "emulator": "http://linserv.ru/Upvel-UR-447N4G/",
        },
        {
          "name": "UPVEl UR-312N4G",
          "pppoe":
            "https://clever.ertelecom.ru/content/space/4/folder/465/article/13750",
          "dhcp": "Нет",
          "ipoe": "https://clever.ertelecom.ru/content/space/4/folder/465/article/13752",
          "channels": "Нет",
          "settings": "10.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2521?text=UPVEl+UR-312N4G",
          "emulator": "http://linserv.ru/Upvel-UR825AC/",
        },
        {
          "name": "Tenda Nova MW3, MW6",
          "pppoe":
            "https://clever.ertelecom.ru/content/space/4/article/1580/page/3?fileView=39281",
          "dhcp": "https://clever.ertelecom.ru/content/space/4/article/1580/page/3?fileView=39282",
          "ipoe": "Нет",
          "channels": "Нет",
          "settings": "0.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2072?text=Tenda+Nova+MW3,+MW6",
          "emulator": "Нет",
        },
        {
          "name": "Tp-Link DECO M4",
          "pppoe":
            "https://clever.ertelecom.ru/content/space/4/article/1564/page/3?fileView=39198",
          "dhcp": "https://clever.ertelecom.ru/content/space/4/article/1564/page/3?fileView=39199",
          "ipoe": "https://clever.ertelecom.ru/content/space/4/article/1564/page/3?fileView=39198",
          "channels": "Нет",
          "settings": "68.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2072?text=Tp-Link+DECO+M4",
          "emulator": "Нет",
        },
        {
            "name": "Nokia Wifi Beacon",
          "pppoe":
            "D0%B8%D0%BD%D1%82%D0%B5%D1%80%D1%84%D0%B5%D0%B9%D1%81.pdf",
          "dhcp": "https://clever.ertelecom.ru/content/space/4/article/1616/page/3?fileView=39298",
          "ipoe": "Нет",
          "channels": "Нет",
          "settings": "18.1",
          "bz": "https://clever.ertelecom.ru/content/space/4/article/2072?text=Nokia+Wifi+Beacon",
          "emulator": "Нет",
        }
]


async def is_user_in_channel(user_id: int, bot):
    channel_id = -1002068999312
    try:
        sub = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        logging.info(sub)
        return sub.status != "left"
    except Exception as e:
        print(f"Произошла ошибка при проверке подписки: {e}")
        return False


@inline_router.inline_query()
async def handle_inline_query(query: InlineQuery, bot: Bot):
    try:
        # Проверка подписки
        if not await is_user_in_channel(query.from_user.id, bot):
            subscription_text = (
                "❗️ Для использования бота требуется подписка на канал\n\n"
                "📢 <b>Не Дом.ру</b>\n"
                "🔗 https://t.me/+F0O_FIydoKg2M2U6\n\n"
                "После подписки вернитесь и попробуйте снова!"
            )
            return await query.answer(
                results=[
                    InlineQueryResultArticle(
                        id="subscribe_required",
                        title="Требуется подписка на канал",
                        description="Подпишитесь на канал Не Дом.ру для доступа к информации",
                        input_message_content=InputTextMessageContent(
                            message_text=subscription_text,
                            parse_mode="HTML",
                            disable_web_page_preview=True
                        )
                    )
                ],
                cache_time=5,
                is_personal=True
            )

        results = []
        search_query = query.query.lower()

        # Если запрос начинается с 'r ' или 'р ' (русская), ищем по роутерам
        if search_query.startswith(('r ', 'р ')):
            search_term = search_query[2:]
            filtered_data = [
                item for item in ROUTER_DATA
                if search_term in item['name'].lower()
            ] if search_term else ROUTER_DATA

            for idx, item in enumerate(filtered_data):
                # Формируем ссылки на настройки
                settings_links = []
                if item.get('pppoe'):
                    settings_links.append("[PPPoE]({})".format(item['pppoe']))
                if item.get('dhcp'):
                    settings_links.append("[DHCP]({})".format(item['dhcp']))
                if item.get('ipoe'):
                    settings_links.append("[IPoE]({})".format(item['ipoe']))

                # Основной текст сообщения
                message_text = (
                    f"📡 *{item['name']}*\n\n"
                    f"⚙️ IP-адрес: `{item['settings']}`\n\n"
                    f"📝 Инструкции по настройке:\n"
                    f"• {' • '.join(settings_links)}\n\n"
                )

                # Добавляем дополнительные ссылки, если они есть
                if item.get('channels'):
                    message_text += f"📶 [Настройка каналов Wi-Fi]({item['channels']})\n"
                if item.get('bz'):
                    message_text += f"📋 [База знаний]({item['bz']})\n"
                if item.get('emulator'):
                    emulator_link = item['emulator'][0] if isinstance(item['emulator'], list) else item['emulator']
                    message_text += f"💻 [Эмулятор настроек]({emulator_link})"

                results.append(
                    InlineQueryResultArticle(
                        id=f"router_{idx}",
                        title=item['name'],
                        description="Нажми для просмотра инструкций по настройке",
                        input_message_content=InputTextMessageContent(
                            message_text=message_text,
                            parse_mode="Markdown",
                            disable_web_page_preview=True
                        )
                    )
                )

        # Если запрос начинается с 'm ' или 'м ' (русская), ищем по MNA
        elif search_query.startswith(('m ', 'м ')):
            search_term = search_query[2:]  # Убираем префикс и пробел
            filtered_data = [
                item for item in MNA_DATA
                if search_term in item['name'].lower() or
                   search_term in item['authorization'].lower() or
                   search_term in item['connection'].lower()
            ] if search_term else MNA_DATA

            for idx, item in enumerate(filtered_data):
                message_text = (
                    f"📡 *{item['name']}*\n\n"
                    f"🔐 Авторизация: {item['authorization']}\n"
                    f"🔌 Подключение: {item['connection']}\n"
                    f"🔗 [Подробнее]({item['link']})"
                )

                results.append(
                    InlineQueryResultArticle(
                        id=f"mna_{idx}",
                        title=item['name'],
                        description=f"Авторизация: {item['authorization']} | Подключение: {item['connection']}",
                        input_message_content=InputTextMessageContent(
                            message_text=message_text,
                            parse_mode="Markdown",
                            disable_web_page_preview=True
                        )
                    )
                )

        # Если нет префикса или пустой запрос, показываем инструкцию
        else:
            results = [
                InlineQueryResultArticle(
                    id="help",
                    title="Как использовать поиск",
                    description="Выбери для просмотра инструкции",
                    input_message_content=InputTextMessageContent(
                        message_text=(
                            "📱 *Как использовать поиск:*\n\n"
                            "• Для поиска по MNA используй префикс `m` или `м`\n"
                            "Пример: `м интерзет` или `m интерзет`\n\n"
                            "• Для поиска по роутерам используй префикс `r` или `р`\n"
                            "Пример: `р dir` или `r dir`"
                        ),
                        parse_mode="Markdown"
                    )
                )
            ]

        if not results:
            results.append(
                InlineQueryResultArticle(
                    id="not_found",
                    title="Ничего не найдено",
                    description="Попробуйте изменить поисковый запрос",
                    input_message_content=InputTextMessageContent(
                        message_text="К сожалению, по вашему запросу ничего не найдено."
                    )
                )
            )

        await query.answer(
            results=results,
            cache_time=300,
            is_personal=True
        )

    except Exception as e:
        print(f"Error in inline query: {e}")
        error_result = InlineQueryResultArticle(
            id="error",
            title="Произошла ошибка",
            description="Не удалось загрузить данные",
            input_message_content=InputTextMessageContent(
                message_text="К сожалению, произошла ошибка при загрузке данных. Попробуйте позже."
            )
        )
        await query.answer(
            results=[error_result],
            cache_time=5
        )

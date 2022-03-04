#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) xmysteriousx

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import asyncio
import json
import shutil

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from pyrogram import Client, filters

@Client.on_message(filters.document & filters.private)
async def extracter(bot, update):
    try:
        json_location = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "/raw.json"
        link_file_location = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "/links.txt"
        tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id)
        await bot.download_media(
            message=update,
            file_name=json_location
        )
        f = open(json_location,'r', encoding = "utf8")
        data = json.loads(f.read())
        for j in data['data']:
            if j['type'] == "Video":
                course_link=j['video_link']
                course_name=j['title']
                try:
                    if "\\" in course_link:
                        course_link = course_link.replace("\\", "")
                except Exception as e:
                    logger.info(e)
                    pass
                try:
                    t = open(link_file_location,"a")
                    t.write(f"{course_name}:{course_link}")
                    t.write("\n")
                except Exception as e:
                    logger.info(e)
                    pass
        f.close()
        t.close()
        await bot.send_document(
            chat_id=update.chat.id,
            document=link_file_location,
            reply_to_message_id=update.message_id
        )
        shutil.rmtree(tmp_directory_for_each_user)
    except Exception as e:
        logger.info(e)
        pass
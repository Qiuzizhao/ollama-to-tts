#!/usr/bin/env python3

import edge_tts
import pygame
import os
import emoji

import re

def remove_colon_words(text):
    # 定义正则表达式模式，匹配两个冒号之间的内容，包括冒号
    pattern = r':[^:]+:'
    
    # 使用re.sub来替换匹配的模式为空字符串
    result = re.sub(pattern, '', text)
    
    # 返回处理后的字符串
    return result

def tts(TEXT):
    """Main function"""
    
    # Remove emojis from the text
    TEXT = emoji.demojize(TEXT).replace("_", "")
    TEXT = remove_colon_words(TEXT)
    # print(TEXT)

    # Rest of the code...
        
    # TEXT = "你好哟，智能语音助手小伊"
    VOICE = "zh-CN-XiaoyiNeural"
    OUTPUT_FILE = "output.mp3"
    
    communicate = edge_tts.Communicate(TEXT, VOICE)
    communicate.save_sync(OUTPUT_FILE)
    
 
    # 初始化pygame
    pygame.init()
 
    # 创建音乐播放器对象
    pygame.mixer.init()
 
    # 加载mp3文件
    pygame.mixer.music.load(OUTPUT_FILE)
 
    # 播放音乐
    pygame.mixer.music.play()
    
    # 等待音乐播放完毕
    while pygame.mixer.music.get_busy():
        continue
 
    # 停止音乐
    pygame.mixer.music.stop()
    
    # 删除mixer对象
    pygame.mixer.quit()
    
    # 删除临时文件
#    os.remove(OUTPUT_FILE)


if __name__ == "__main__":
    while True:
        user_input = input("\n请输入：")
        tts(user_input)

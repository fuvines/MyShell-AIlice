import time
from termcolor import colored

from common.AConfig import config
from core.AProcessor import AProcessor
from llm.ALLMPool import llmPool
from utils.ALogger import ALogger
from modules.ARemoteAccessors import *
from AServices import StartServices

from prompts.APrompts import promptsManager
from prompts.APromptChat import APromptChat
from prompts.APromptMain import APromptMain
from prompts.APromptSystem import APromptSystem
from prompts.APromptRecurrent import APromptRecurrent
from prompts.APromptCoder import APromptCoder
from prompts.APromptCoderProxy import APromptCoderProxy
from prompts.APromptArticleDigest import APromptArticleDigest


def GetInput() -> str:
    if config.speechOn:
        print(colored("USER: ", "green"), end="", flush=True)
        inp = speech.GetAudio()
        print(inp, end="", flush=True)
        print("")
    else:
        inp = input(colored("USER: ", "green"))
    return inp

def main(modelID: str, quantization: str, maxMemory: dict, prompt: str, temperature: float, flashAttention2: bool, speechOn: bool):
    config.Initialize()
    config.quantization = quantization
    config.maxMemory = maxMemory
    config.temperature = temperature
    config.flashAttention2 = flashAttention2
    config.speechOn = speechOn
    
    StartServices()
    speech.Enable(config.speechOn)
    
    for promptCls in [APromptChat, APromptMain, APromptSystem, APromptRecurrent, APromptCoder, APromptCoderProxy, APromptArticleDigest]:
        promptsManager.RegisterPrompt(promptCls)
    
    llmPool.Init([modelID, "oai:gpt-3.5-turbo", "oai:gpt-4"])
    
    logger = ALogger(speech=speech)
    processor = AProcessor(modelID=modelID, promptName=prompt, outputCB=logger.Receiver, collection="ailice" + str(time.time()))
    while True:
        inpt = GetInput()
        processor(inpt)
    return

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--modelID',type=str,default='hf:Open-Orca/Mistral-7B-OpenOrca')
    parser.add_argument('--quantization',type=str,default='')
    parser.add_argument('--maxMemory',type=dict,default=None)
    parser.add_argument('--prompt',type=str,default='main')
    parser.add_argument('--temperature',type=float,default=0.0)
    parser.add_argument('--flashAttention2',type=bool,default=False)
    parser.add_argument('--speechOn',type=bool,default=False)
    kwargs = vars(parser.parse_args())
    main(**kwargs)
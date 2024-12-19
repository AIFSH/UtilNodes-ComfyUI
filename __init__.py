import os
import folder_paths
now_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = folder_paths.get_input_directory()
output_dir = folder_paths.get_output_directory()
import torch
import tempfile
import torchaudio
from PIL import Image
import numpy as np
class GetRGBEmptyImgae:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT",{"default": 512, "min": 128, "max": 1024, "step": 64, "display": "number"}),
                "height":("INT",{"default": 512, "min": 128, "max": 1024, "step": 64, "display": "number"}),
                "R":("INT",{"default": 124, "min": 0, "max": 255, "step": 1, "display": "number"}),
                "G":("INT",{"default": 252, "min": 0, "max": 255, "step": 1, "display": "number"}),
                "B":("INT",{"default": 0, "min": 0, "max": 255, "step": 1, "display": "number"}),
            }
        }
    RETURN_TYPES = ("IMAGE",)
    
    FUNCTION = "gen_img"

    CATEGORY = "AIFSH_UtilNodes"
    def gen_img(self,width,height,R,G,B):
        new_image = Image.new("RGB",(width,height),color=(R,G,B))
        return (torch.from_numpy(np.asarray(new_image)/255.0).unsqueeze(0),)



class PromptTextNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "dynamicPrompts": True, "tooltip": "The text to be encoded."}), 
            }
        }
    RETURN_TYPES = ("TEXT",)
    
    FUNCTION = "encode"

    CATEGORY = "AIFSH_UtilNodes"
    # DESCRIPTION = "Encodes a text prompt using a CLIP model into an embedding that can be used to guide the diffusion model towards generating specific images."

    def encode(self, text):
        return (text, )

class LoadVideo:
    @classmethod
    def INPUT_TYPES(s):
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and f.split('.')[-1] in ["mp4", "webm","mkv","avi"]]
        return {"required":{
            "video":(files,),
        },
        }
    
    CATEGORY = "AIFSH_UtilNodes"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ("VIDEO","AUDIO",)

    OUTPUT_NODE = False

    FUNCTION = "load_video"

    def load_video(self, video,ffmpeg_audio=None):
        video_path = os.path.join(input_dir,video)
    
        with tempfile.NamedTemporaryFile(suffix=".wav",dir=input_dir,delete=False) as aud:
            os.system(f"""ffmpeg -i {video_path} -vn -acodec pcm_s16le -ar 44100 -ac 1 {aud.name} -y""")
        waveform, sample_rate = torchaudio.load(aud.name)
        audio = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
        
        return (video_path,audio,)

class PreViewVideo:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
            "video":("VIDEO",),
        }}
    
    CATEGORY = "AIFSH_UtilNodes"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ()

    OUTPUT_NODE = True

    FUNCTION = "load_video"

    def load_video(self, video):
        video_name = os.path.basename(video)
        video_path_name = os.path.basename(os.path.dirname(video))
        return {"ui":{"video":[video_name,video_path_name]}}

WEB_DIRECTORY = "./js"

NODE_CLASS_MAPPINGS = {
    "LoadVideo":LoadVideo,
    "PreViewVideo":PreViewVideo,
    "PromptTextNode": PromptTextNode,
    "GetRGBEmptyImgae":GetRGBEmptyImgae
}
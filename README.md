# **Real-time Translator**:
### It's a real-time speach-to-text, speach-to-speach translator with the optional avatar that can lipsync real time. The backbone of this web-app is OpenAI whisper, and translator api, and the web-app developed using streamlit.
To start the program, install the requirements.txt on your directory using "pip install -requirements.txt".


[Paper](http://arxiv.org/abs/2008.10010) | [Project Page](http://cvit.iiit.ac.in/research/projects/cvit-projects/a-lip-sync-expert-is-all-you-need-for-speech-to-lip-generation-in-the-wild/) | [Demo Video](https://youtu.be/0fXaDCZNOJc) | 
 
----------
**Highlights**
----------
- `Python 3.6` 
- ffmpeg: `sudo apt-get install ffmpeg`
- Install necessary packages using `pip install -r requirements.txt`. Alternatively, instructions for using a docker image is provided [here](https://gist.github.com/xenogenesi/e62d3d13dadbc164124c830e9c453668). Have a look at [this comment](https://github.com/Rudrabha/Wav2Lip/issues/131#issuecomment-725478562) and comment on [the gist](https://gist.github.com/xenogenesi/e62d3d13dadbc164124c830e9c453668) if you encounter any issues. 
- Face detection [pre-trained model](https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth) should be downloaded to `face_detection/detection/sfd/s3fd.pth`. Alternative [link](https://iiitaphyd-my.sharepoint.com/:u:/g/personal/prajwal_k_research_iiit_ac_in/EZsy6qWuivtDnANIG73iHjIBjMSoojcIV0NULXV-yiuiIg?e=qTasa8) if the above does not work.
Getting the weights
----------
| Model  | Description |  Link to the model | 
| :-------------: | :---------------: | :---------------: |
| Wav2Lip  | Highly accurate lip-sync | [Link](https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/Eb3LEzbfuKlJiR600lQWRxgBIY27JZg80f7V9jtMfbNDaQ?e=TBFBVW)  |
| Wav2Lip + GAN  | Slightly inferior lip-sync, but better visual quality | [Link](https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/EdjI7bZlgApMqsVoEUUXpLsBxqXbn5z8VTmoxp55YNDcIA?e=n9ljGW) |
| Expert Discriminator  | Weights of the expert discriminator | [Link](https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/EQRvmiZg-HRAjvI6zqN9eTEBP74KefynCwPWVmF57l-AYA?e=ZRPHKP) |
| Visual Quality Discriminator  | Weights of the visual disc trained in a GAN setup | [Link](https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/EQVqH88dTm1HjlK11eNba5gBbn15WMS0B0EZbDBttqrqkg?e=ic0ljo) |
Lip-syncing videos using the pre-trained models (Inference)
-------

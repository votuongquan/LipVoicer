from .nnet import AudioEfficientConformerInterCTC
from .nnet import CTCLoss, CTCBeamSearchDecoder
import sentencepiece as spm


def get_models(dataset):
    assert dataset.lower() in ['lrs3', 'lrs2'], 'Dataset must be LRS3 or LRS2'
    asr_guidance_net = AudioEfficientConformerInterCTC(
        interctc_blocks=[], T=400, beta_0=0.0001, beta_T=0.02)
    checkpoint_ao = f"/content/drive/MyDrive/LipVoicerCheckpoints/checkpoints_ft_lrs3.ckpt"
    asr_guidance_net.compile(losses=CTCLoss(
        zero_infinity=True, assert_shorter=False), loss_weights=None)
    asr_guidance_net = asr_guidance_net.cuda()
    asr_guidance_net.load(checkpoint_ao)
    asr_guidance_net.eval()
    tokenizer_path = "/content/drive/MyDrive/LipVoicerCheckpoints/tokenizerbpe256.model"
    tokenizer = spm.SentencePieceProcessor(
        tokenizer_path)  # for converting text to tokens
    ngram_path = "/content/drive/MyDrive/LipVoicerCheckpoints/6gram_lrs23.arpa"
    neural_config_path = "ASR/configs/LRS23/LM/GPT-Small-demo.py"
    neural_checkpoint = "/content/drive/MyDrive/LipVoicerCheckpoints/checkpoints_epoch_10_step_2860.ckpt"

    # Decoder for converting tokens to text at the ASR output
    decoder = CTCBeamSearchDecoder(
        tokenizer_path=tokenizer_path,
        ngram_path=ngram_path,
        neural_config_path=neural_config_path,
        neural_checkpoint=neural_checkpoint,
    )

    return asr_guidance_net, tokenizer, decoder

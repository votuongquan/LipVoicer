import sys

# sys.path.append("../../")

# Imports
from ASR import nnet
import torch

# Architecture
vocab_size = 1024
model = "GPT-Small"
max_pos_encoding = 2048
pad_token = 0
sos_token = vocab_size
eos_token = vocab_size

# Pretrained Checkpoint
pretrained = False
pretrained_checkpoint = (
    "callbacks/LibriSpeechCorpus/GPT-Small/checkpoints_epoch_13_step_512924.ckpt"
)

# Training
lr = 6e-5
epochs = 10
batch_size = 128
accumulated_steps = 2
tokenizer_path = "/content/drive/MyDrive/LipVoicerCheckpoints/tokenizerbpe1024.model"
precision = torch.float16
callback_path = "ASR/callbacks/LRS23/LM/GPT-Small"

# Model
model = nnet.GPT(
    vocab_size=vocab_size + 1,
    padding_idx=pad_token,
    max_pos_encoding=max_pos_encoding,
    model=model,
    pos_embedding=nnet.SinPosEmbedding,
)
model.compile(
    optimizer=nnet.AdamW(
        params=nnet.get_decay_param_groups(model, weight_decay=0.1),
        lr=lr,
        betas=(0.9, 0.95),
        eps=1e-8,
    )
)

# Load Pretrained
if pretrained:
    model.load_state_dict(
        torch.load(pretrained_checkpoint, map_location=model.device)[
            "model_state_dict"]
    )

# Datasets
label_max_length = 100
collate_fn = nnet.CollateFn(
    inputs_params=[
        {
            "axis": 0,
            "padding": True,
            "start_token": sos_token,
            "padding_value": pad_token,
        }
    ],
    targets_params=[
        {"axis": 0, "padding": True, "end_token": eos_token, "padding_value": -1}
    ],
)

# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from fairseq.modules import (
    LayerNorm,
    TransformerEncoderLayer,
    TransformerDecoderLayer
)

from . import build_monotonic_attention


class TransformerMonotonicEncoderLayer(TransformerEncoderLayer):

    def forward(self, x, encoder_padding_mask):
        seq_len, _, _ = x.size()
        attn_mask = x.new_ones([seq_len, seq_len]).tril(-1)
        attn_mask = attn_mask.masked_fill(attn_mask.bool(), float('-inf'))
        return super().forward(x, encoder_padding_mask, attn_mask)


class TransformerMonotonicDecoderLayer(TransformerDecoderLayer):

    def __init__(self, args, no_encoder_attn=False, add_bias_kv=False, add_zero_attn=False):
        super().__init__(
            args,
            no_encoder_attn=True,
            add_bias_kv=add_bias_kv,
            add_zero_attn=add_zero_attn
        )
        self.encoder_attn = build_monotonic_attention(args)
        self.encoder_attn_layer_norm = LayerNorm(
            self.embed_dim,
            export=getattr(args, 'char_inputs', False)
        )
    
    
    


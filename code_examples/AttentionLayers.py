class AttentionLayer(torch.nn.Module):
    def __init__(self, feature_dim, weight_dim, device):
        super(AttentionLayer, self).__init__()
        self.in_dim = feature_dim
        self.device = device

        self.Q = xavier_init(nn.Linear(self.in_dim, weight_dim))
        self.K = xavier_init(nn.Linear(self.in_dim, weight_dim))
        self.V = xavier_init(nn.Linear(self.in_dim, weight_dim))

        self.feature_dim = weight_dim

    def forward(self, x):
        '''
        inference
        :param x: [num_agent, num_target, feature_dim]
        :return z: [num_agent, num_target, weight_dim]
        '''
        # z = softmax(Q,K)*V
        q = torch.tanh(self.Q(x))  # [batch_size, sequence_len, weight_dim]
        k = torch.tanh(self.K(x))  # [batch_size, sequence_len, weight_dim]
        v = torch.tanh(self.V(x))  # [batch_size, sequence_len, weight_dim]

        z = torch.bmm(F.softmax(torch.bmm(q, k.permute(0, 2, 1)), dim=2), v)  # [batch_size, sequence_len, weight_dim]

        global_feature = z.sum(dim=1)
        return z, global_feature

    
    
    
class ScaledDotProductAttention(nn.Module):
  
    def __init__(self):
        super(ScaledDotProductAttention, self).__init__()
        self.softmax = nn.Softmax()

    def forward(self, q, k, v, mask=None, e=1e-12):
        batch_size, head, length, d_tensor = k.size()

        # 1. dot product Query with Key^T to compute similarity
        k_t = k.view(batch_size, head, d_tensor, length) 
        score = (q @ k_t) / math.sqrt(d_tensor) 

        # 2. apply masking (opt)
        if mask is not None:
            score = score.masked_fill(mask == 0, -e)

        # 3. pass them softmax to make [0, 1] range
        score = self.softmax(score)

        # 4. multiply with Value
        v = score @ v

        return v, score
class MultiHeadAttention(nn.Module):
    def __init__(self, model_dim, n_head, dropout_rate):
        super(MultiHeadAttention, self).__init__()

        self.model_dim=model_dim
        self.n_head=n_head
        self.head_dim = self.model_dim // self.n_head

        self.linear_k = nn.Linear(self.model_dim, self.head_dim * self.n_head) 
        self.linear_v = nn.Linear(self.model_dim, self.head_dim * self.n_head) 
        self.linear_q = nn.Linear(self.model_dim, self.head_dim * self.n_head)

        self.linear_final=nn.Linear(self.head_dim * self.n_head, self.model_dim)
        self.dropout = nn.Dropout(dropout_rate)
        self.scaled_dot_product_attention = ScaledDotProductAttention(dropout_rate)


    def forward(self, query, key, value, mask=None):
        q = self.linear_q(query) 
        k = self.linear_k(key)
        v = self.linear_v(value)
        batch_size=k.size()[0]

        q_ = q.view(batch_size * self.n_head, -1, self.head_dim) 
        k_ = k.view(batch_size * self.n_head, -1, self.head_dim)
        v_ = v.view(batch_size * self.n_head, -1, self.head_dim)

        context = self.scaled_dot_product_attention(q_, k_, v_, mask) 

        output = context.view(batch_size, -1, self.head_dim * self.n_head) 
        output = self.linear_final(output)
        output = self.dropout(output)
        return output

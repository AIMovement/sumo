import torch
import torch.nn as nn

class DQN(nn.Module):
    def __init__(self, input_shape, n_actions):
        super(DQN, self).__init__()

        self.fc = nn.Sequential(
            nn.Linear(input_shape[0], 32),
            nn.ReLU(),
            #nn.Linear(32, 32),
            #nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, n_actions)
        )

    def forward(self, x):
        return self.fc(x)

class DuelingDQN(nn.Module):
    def __init__(self, input_shape, n_actions):
        super(DuelingDQN, self).__init__()

        self.fc_adv = nn.Sequential(
            nn.Linear(input_shape[0], 32),
            nn.ReLU(),
            #nn.Linear(32, 32),
            #nn.ReLU(),
            nn.Linear(32, n_actions)
        )

        self.fc_val = nn.Sequential(
            nn.Linear(input_shape[0], 32),
            nn.ReLU(),
            #nn.Linear(32, 32),
            #nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        adv = self.fc_adv(x)
        return self.fc_val(x) + adv - adv.mean()

# args

```python
# WandB
    parser.add_argument('--with-wandb', default=False, action='store_true', help='Enables Weights and Biases')
    parser.add_argument('--wandb-entity', default='', type=str, help='WandB username (entity).')
    parser.add_argument('--wandb-project', default='', type=str, help='WandB "Project"')
    parser.add_argument('--wandb-group', default=None, type=str, help='WandB "Group". Name of the env by default.')
    parser.add_argument('--wandb-job_type', default='train', type=str, help='WandB job type')
    parser.add_argument('--wandb-tags', default=[], type=str, nargs='*', help='Tags can help finding experiments')
    parser.add_argument('--wandb-key', default=None, type=str, help='API key for authorizing WandB')
    parser.add_argument('--wandb-dir', default=None, type=str, help='the place to save WandB files')
    parser.add_argument('--wandb-experiment', default='', type=str, help='Identifier to specify the experiment')

```

# install wandb & login

# import wandb
```
from wandb_utils import init_wandb
init_wandb(args)
```

# log
```
info_dict = {}
info_dict['acc'] = 0.1

# wandb.log(info_dict)
wandb.log(info_dict, step=epoch)
```

from tensorboard.backend.event_processing import event_accumulator as ea
import matplotlib.pyplot as plt
import numpy as np
import os   
import ipdb

# parent_path = "/home/zyd/Reed/RL/AD_VAT_PPO/logs/UnrealTrack-DuelingRoomNav-DiscreteColor-v4/baseline_no_reward_regression/Agent:0"

# save_name = "train_reward_baseline.npy"

def save_tensorboard_as_np(parent_path, name, save_name):
    file_path = os.path.join(parent_path, os.listdir(parent_path)[0])
    parent_path = os.path.dirname(parent_path)
    temp = ea.EventAccumulator(file_path)
    temp.Reload()
    print(temp.scalars.Keys())
    content = temp.scalars.Items(name)
    np.save(os.path.join(parent_path, save_name), content)


def plot_cur(models, name, save_name, n=None):

    fig = plt.figure(num=1, dpi=200)
    plt.ylabel(name)
    plt.xlabel("iteractions")
    plt.title("Cumulative rewards")

    
    content = []
    for f in models:
    
        temp = np.load(os.path.join(parent_path, f, f+".npy"))
        step = np.array([i[1] for i in temp])
        content = np.array([i[2] for i in temp])
        
        if n is not None:
            content=np.convolve(content, np.ones((n,))/n, mode="same")
        plt.plot(step, content)

    plt.legend(models,loc='best')
    plt.savefig(save_name, dpi=600)

    
name = 'test/reward0'
parent_path = "/home/zyd/Reed/RL/AD_VAT_PPO/logs/UnrealTrack-DuelingRoomNav-DiscreteColor-v4/"
models = {"baseline", "baseline_no_reward_regression", "real_bbox_to_critic_pred_bbox_to_actor", "re_bbox_no_action", "re_bbox_using_action"}
for f in models:
    save_tensorboard_as_np(os.path.join(parent_path, f, "Test"), name, f+".npy")

plot_cur(models, name, "training_stage.jpg", 50)



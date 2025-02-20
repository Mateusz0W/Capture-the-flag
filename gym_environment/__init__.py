from gym.envs.registration import register

register(
    id='gym_environment/Capture-the-flag-v0',
    entry_point='gym_environment.environment:Environment',
    max_episode_steps=500,
)
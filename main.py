import gym
import gym_environment

if __name__=="__main__":
    env=gym.make('gym_environment/Capture-the-flag-v0',render_mode='human')
    
    obs, info = env.reset()  # Reset środowiska
    print("Początkowa obserwacja:\n", obs)
    print("Informacje:\n", info)

    for i in range(1000):
        action = env.action_space.sample()  # Losowa akcja
        obs, reward, done, _, info = env.step(action)  # Wykonanie akcji

    print("\nObserwacja po wykonaniu akcji:\n", obs)
    print("Nagroda:", reward)
    print("Czy koniec gry:", done)
    print("Dodatkowe info:", info)
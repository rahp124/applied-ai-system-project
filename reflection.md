# Profile Comparison Reflection

## High-Energy Pop vs Chill Lofi

- High-Energy Pop surfaces tracks like **Sunrise City** and **Gym Hero** because they combine high energy with low acousticness.
- Chill Lofi shifts toward **Library Rain**, **Focus Flow**, and **Midnight Coding**, which have lower energy and higher acousticness.
- This makes sense because the profiles differ strongly on `target_energy` and `likes_acoustic`, so the scorer rewards opposite ends of the catalog.

## High-Energy Pop vs Deep Intense Rock

- Both profiles return high-energy, non-acoustic songs, so there is overlap (for example, **Sunrise City** and **Gym Hero** still appear).
- Deep Intense Rock pushes **Storm Runner** to the top because it matches both rock genre and intense mood.
- This makes sense because the two profiles share similar energy/acoustic targets, but differ on genre and mood labels.

## Chill Lofi vs Deep Intense Rock

- Chill Lofi prioritizes calm, acoustic, low-energy songs, while Deep Intense Rock prioritizes intense, non-acoustic, high-energy songs.
- Their top results are clearly separated (e.g., **Library Rain** vs **Storm Runner**), showing the model reacts to opposing preference settings.
- This contrast is valid because the profiles intentionally test opposite listening contexts, and the output shifts accordingly.

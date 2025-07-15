# Useful Links for Stickman Physics Dev

- [Pymunk Documentation](http://www.pymunk.org/en/latest/)
- [Pygame Docs](https://www.pygame.org/docs/)
- [Box2D vs Chipmunk (Comparison)](https://www.iforce2d.net/b2dtut/physics)
- [Gamasutra – Ragdoll Physics in Games](https://www.gamedeveloper.com/programming/character-physics-in-modern-games)

---

- [github.com/bepu/bepuphysics2](https://github.com/bepu/bepuphysics2)
- [github.com/savant117](https://github.com/savant117/avbd-demo2d)
- [AVBD 2D Demo](https://graphics.cs.utah.edu/research/projects/avbd/avbd_demo2d.html)

---

  Interesting Soft Body scene from the savant117/avbd-demo2d
```cpp
static void sceneSoftBody(Solver* solver)
{
    solver->clear();
    new Rigid(solver, { 100, 0.5f }, 0.0f, 0.5f, { 0.0f, 0.0f });

    const float Klin = 1000.0f;
    const float Kang = 100.0f;
    const int W = 15, H = 5;
    const int N = 2;
    for (int i = 0; i < N; i++)
    {
        Rigid* grid[W][H];
        for (int x = 0; x < W; x++)
            for (int y = 0; y < H; y++)
                grid[x][y] = new Rigid(solver, { 1, 1 }, 1.0f, 0.5f, { (float)x, (float)y + H * i * 2.0f + 5.0f, 0.0f });

        for (int x = 1; x < W; x++)
            for (int y = 0; y < H; y++)
                new Joint(solver, grid[x - 1][y], grid[x][y], { 0.5f, 0 }, { -0.5f, 0 }, { Klin, Klin, Kang });

        for (int x = 0; x < W; x++)
            for (int y = 1; y < H; y++)
                new Joint(solver, grid[x][y - 1], grid[x][y], { 0, 0.5f }, { 0, -0.5f }, { Klin, Klin, Kang });

        for (int x = 1; x < W; x++)
        {
            for (int y = 1; y < H; y++)
            {
                new IgnoreCollision(solver, grid[x - 1][y - 1], grid[x][y]);
                new IgnoreCollision(solver, grid[x][y - 1], grid[x - 1][y]);
            }
        }
    }
}
```

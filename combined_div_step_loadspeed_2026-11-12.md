# Division, step and LoadSpeed: Leonid's and Claude's runs together (12 Nov 2026)

Same model in both: Radu's buffed Nokian JSON (900 kPa, Distributed, E 2e8, Reference Divisions 40, Stiff true), EULER_IMPLICIT_LINEARIZED, Pardiso MKL, NODE_CLOUD 0.02, plate E 2e9, drop speed 0.1, 0.25 s pause, all 9 loads. Averaging window 5 ms unless the window column says otherwise. The column gives the window in ms and, in brackets, in steps (steps = window / step, so 5 ms is 50 steps at 1e-4 but 500 steps at 1e-5). Only division, step, LoadSpeed and window differ.
- **Leonid**: his PC, threads Chrono 4 / collision 4 / Pardiso 8, step 1e-4.
- **Claude**: cloud machine (4 cores), Chrono feature/mb_tire e359e2f built with Pardiso; 1 thread per run and 4 runs side by side unless the threads column says otherwise.
- Times from different machines or thread settings can't be compared with each other.
- **ref** = the best converged case: 120 div, step 1e-5, LoadSpeed 0.01. "max diff vs ref" is the largest difference over the 9 loads, in mm. RMS vs data is over the first 8 loads.
- "blows up": the load shoots past the remaining targets while the deflection stops growing.

## Deflection in mm at each load (kg)

| div     | step   | LoadSpeed | window ms (steps) | who             | 902.9    | 1358.7 | 1812.3 | 2251.1 | 2704.5 | 3165.8 | 3614.3 | 4069.9 | 4501.1 | max diff vs ref | RMS vs data | time   | threads |
|---------|--------|-----------|-------------------|-----------------|----------|--------|--------|--------|--------|--------|--------|--------|--------|-----------------|-------------|--------|---------|
| data    |        |           |                   |                 | 8.2      | 12.1   | 16.0   | 19.6   | 23.3   | 27.0   | 30.5   | 34.0   | 36.5   |                 |             |        |         |
| **ref** | 1e-5   | 0.01      | 5 (500)           | Claude, 120 div | 10.69    | 14.05  | 17.14  | 20.19  | 23.49  | 26.66  | 29.69  | 32.78  | 35.81  | 0               | 1.32        |        |         |
| 40      | 4e-4   | 0.01      | 4.8 (12)          | Claude          | blows up |        |        |        |        |        |        |        |        |                 |             | 23 s   | 1/1/1   |
| 40      | 2e-4   | 0.01      | 5 (25)            | Claude          | 9.17     | 12.69  | 17.13  | 21.14  | 23.89  | 26.66  | 29.35  | 32.12  | 34.87  | 1.52            | 1.13        | 69 s   | 1/1/1   |
| 40      | 1e-4   | 0.001     | 5 (50)            | Leonid          | 9.28     | 12.75  | 17.26  | 21.19  | 23.92  | 26.68  | 29.42  | 32.26  | 35.04  | 1.41            | 1.14        | 2401 s | 4/4/8   |
| 40      | 1e-4   | 0.005     | 5 (50)            | Leonid          | 9.28     | 12.74  | 17.25  | 21.19  | 23.92  | 26.68  | 29.42  | 32.26  | 35.04  | 1.41            | 1.14        | 661 s  | 4/4/8   |
| 40      | 1e-4   | 0.01      | 5 (50)            | Claude          | 9.28     | 12.70  | 17.25  | 21.19  | 23.92  | 26.68  | 29.42  | 32.26  | 35.04  | 1.41            | 1.13        | 138 s  | 1/1/1   |
| 40      | 1e-4   | 0.01      | 5 (50)            | Leonid          | 9.28     | 12.73  | 17.25  | 21.19  | 23.92  | 26.68  | 29.42  | 32.26  | 35.04  | 1.41            | 1.14        | –      | 4/4/8   |
| 40      | 1e-4   | 0.02      | 5 (50)            | Leonid          | 9.28     | 12.17  | 17.22  | 21.18  | 23.92  | 26.68  | 29.41  | 32.26  | 35.04  | 1.88            | 1.11        | 205 s  | 4/4/8   |
| 40      | 1e-4   | 0.05      | 5 (50)            | Leonid          | 9.25     | 12.14  | 16.91  | 21.22  | 23.91  | 26.67  | 29.41  | 32.25  | 35.03  | 1.91            | 1.08        | 87 s   | 4/4/8   |
| 40      | 1e-4   | 0.05      | 50 (500)          | Leonid          | 9.28     | 12.22  | 17.18  | 21.15  | 23.91  | 26.68  | 29.41  | 32.26  | 35.03  | 1.83            | 1.10        | 88 s   | 4/4/8   |
| 40      | 1e-4   | 0.1       | 5 (50)            | Claude          | 9.15     | 12.07  | 16.88  | 21.26  | 24.04  | 26.80  | 29.43  | 32.25  | 34.98  | 1.98            | 1.07        | 55 s   | 1/1/1   |
| 40      | 1e-4   | 0.1       | 5 (50)            | Leonid          | 9.15     | 12.07  | 17.02  | 21.35  | 24.06  | 26.73  | 29.33  | 32.19  | 34.96  | 1.98            | 1.13        | 118 s  | 4/4/8   |
| 40      | 1e-4   | 0.1       | 50 (500)          | Leonid          | 9.28     | 12.22  | 17.01  | 21.00  | 23.88  | 26.67  | 29.41  | 32.26  | 35.03  | 1.83            | 1.05        | 94 s   | 4/4/8   |
| 40      | 5e-5   | 0.01      | 5 (100)           | Claude          | 9.29     | 12.70  | 17.26  | 21.19  | 23.93  | 26.69  | 29.42  | 32.27  | 35.05  | 1.40            | 1.14        | 280 s  | 1/1/1   |
| 40      | 2.5e-5 | 0.01      | 5 (200)           | Claude          | 9.29     | 12.69  | 17.26  | 21.19  | 23.93  | 26.69  | 29.42  | 32.27  | 35.04  | 1.40            | 1.13        | 570 s  | 1/1/1   |
| 60      | 4e-4   | 0.01      | 4.8 (12)          | Claude          | blows up |        |        |        |        |        |        |        |        |                 |             | 30 s   | 1/1/1   |
| 60      | 2e-4   | 0.01      | 5 (25)            | Claude          | 10.45    | 13.84  | 16.85  | 19.83  | 22.88  | 26.19  | 29.70  | 33.09  | 36.05  | 0.61            | 1.18        | 105 s  | 1/1/1   |
| 60      | 1e-4   | 0.01      | 5 (50)            | Claude          | 10.47    | 14.04  | 17.09  | 20.04  | 23.13  | 26.36  | 29.61  | 33.08  | 36.07  | 0.36            | 1.24        | 211 s  | 1/1/1   |
| 60      | 5e-5   | 0.01      | 5 (100)           | Claude          | 10.49    | 14.05  | 17.10  | 20.05  | 23.14  | 26.37  | 29.62  | 33.09  | 36.08  | 0.35            | 1.25        | 433 s  | 1/1/1   |
| 80      | 4e-4   | 0.01      | 4.8 (12)          | Claude          | blows up |        |        |        |        |        |        |        |        |                 |             | 34 s   | 1/1/1   |
| 80      | 2e-4   | 0.01      | 5 (25)            | Claude          | 10.33    | 13.48  | 16.80  | 20.03  | 23.32  | 26.28  | 29.21  | 32.19  | 35.22  | 0.59            | 1.26        | 136 s  | 1/1/1   |
| 80      | 2e-4   | 0.05      | 5 (25)            | Leonid          | 10.33    | 13.55  | 16.76  | 20.15  | 23.37  | 26.32  | 29.10  | 32.29  | 35.14  | 0.67            | 1.27        | 130 s  | 4/4/8   |
| 80      | 1e-4   | 0.001     | 5 (50)            | Leonid          | 10.60    | 13.86  | 17.12  | 20.31  | 23.54  | 26.57  | 29.59  | 32.75  | 35.81  | 0.19            | 1.29        | 4853 s | 4/4/8   |
| 80      | 1e-4   | 0.005     | 5 (50)            | Leonid          | 10.60    | 13.86  | 17.12  | 20.31  | 23.54  | 26.57  | 29.59  | 32.75  | 35.82  | 0.19            | 1.29        | 1087 s | 4/4/8   |
| 80      | 1e-4   | 0.01      | 5 (50)            | Claude          | 10.60    | 13.86  | 17.12  | 20.31  | 23.54  | 26.57  | 29.59  | 32.75  | 35.82  | 0.19            | 1.29        | 275 s  | 1/1/1   |
| 80      | 1e-4   | 0.01      | 5 (50)            | Leonid          | 10.60    | 13.86  | 17.12  | 20.31  | 23.54  | 26.57  | 29.59  | 32.75  | 35.82  | 0.19            | 1.29        | 591 s  | 4/4/8   |
| 80      | 1e-4   | 0.02      | 5 (50)            | Claude          | 10.60    | 13.86  | 17.11  | 20.31  | 23.54  | 26.57  | 29.59  | 32.75  | 35.81  | 0.19            | 1.29        | 193 s  | 2/2/2   |
| 80      | 1e-4   | 0.02      | 5 (50)            | Leonid          | 10.60    | 13.86  | 17.11  | 20.31  | 23.54  | 26.57  | 29.59  | 32.75  | 35.81  | 0.19            | 1.29        | 400 s  | 4/4/8   |
| 80      | 1e-4   | 0.05      | 5 (50)            | Leonid          | 10.60    | 13.85  | 17.11  | 20.31  | 23.52  | 26.56  | 29.58  | 32.74  | 35.81  | 0.20            | 1.29        | 245 s  | 4/4/8   |
| 80      | 1e-4   | 0.05      | 50 (500)          | Leonid          | 10.59    | 13.85  | 17.11  | 20.31  | 23.52  | 26.56  | 29.58  | 32.74  | 35.81  | 0.20            | 1.28        | 169 s  | 4/4/8   |
| 80      | 1e-4   | 0.1       | 5 (50)            | Claude          | 10.58    | 13.79  | 17.06  | 20.30  | 23.52  | 26.55  | 29.57  | 32.73  | 35.80  | 0.26            | 1.27        | 104 s  | 2/2/2   |
| 80      | 1e-4   | 0.1       | 5 (50)            | Leonid          | 10.58    | 13.79  | 17.06  | 20.30  | 23.52  | 26.55  | 29.57  | 32.73  | 35.80  | 0.26            | 1.27        | 182 s  | 4/4/8   |
| 80      | 1e-4   | 0.1       | 50 (500)          | Leonid          | 10.55    | 13.85  | 17.10  | 20.29  | 23.48  | 26.55  | 29.57  | 32.74  | 35.80  | 0.20            | 1.27        | 156 s  | 4/4/8   |
| 80      | 1e-4   | 0.1       | 500 (5000)        | Leonid          | 8.86     | 12.46  | 16.00  | 19.38  | 22.81  | 26.28  | 29.52  | 32.73  | 35.75  | 1.83            | 0.70        | 146 s  | 4/4/8   |
| 80      | 5e-5   | 0.01      | 5 (100)           | Claude          | 10.61    | 13.87  | 17.12  | 20.32  | 23.55  | 26.58  | 29.60  | 32.76  | 35.82  | 0.18            | 1.29        | 558 s  | 1/1/1   |
| 80      | 1e-5   | 0.01      | 5 (500)           | Claude          | 10.59    | 13.85  | 17.11  | 20.31  | 23.53  | 26.56  | 29.58  | 32.74  | 35.81  | 0.20            | 1.28        | 3147 s | 1/1/1   |
| 80      | 1e-5   | 0.05      | 50 (5000)         | Leonid          | 10.58    | 13.84  | 17.10  | 20.30  | 23.51  | 26.55  | 29.57  | 32.74  | 35.80  | 0.21            | 1.28        | 2451 s | 4/4/8   |
| 120     | 4e-4   | 0.01      | 4.8 (12)          | Claude          | blows up |        |        |        |        |        |        |        |        |                 |             | 37 s   | 1/1/1   |
| 120     | 2e-4   | 0.01      | 5 (25)            | Claude          | blows up |        |        |        |        |        |        |        |        |                 |             | 121 s  | 1/1/1   |
| 120     | 1e-4   | 0.005     | 5 (50)            | Leonid          | 10.68    | 14.02  | 17.14  | 20.15  | 23.41  | 26.60  | 29.68  | 32.77  | 35.70  | 0.11            | 1.31        | 1755 s | 4/4/8   |
| 120     | 1e-4   | 0.01      | 5 (50)            | Claude          | 10.67    | 14.02  | 17.14  | 20.15  | 23.41  | 26.60  | 29.68  | 32.77  | 35.69  | 0.12            | 1.31        | 412 s  | 1/1/1   |
| 120     | 1e-4   | 0.01      | 5 (50)            | Leonid          | 10.67    | 14.02  | 17.14  | 20.15  | 23.41  | 26.60  | 29.68  | 32.77  | 35.69  | 0.12            | 1.31        | 1012 s | 4/4/8   |
| 120     | 1e-4   | 0.02      | 5 (50)            | Leonid          | 10.67    | 14.01  | 17.14  | 20.15  | 23.41  | 26.60  | 29.67  | 32.77  | 35.69  | 0.12            | 1.31        | 637 s  | 4/4/8   |
| 120     | 1e-4   | 0.05      | 50 (500)          | Leonid          | 10.67    | 14.01  | 17.12  | 20.15  | 23.41  | 26.59  | 29.66  | 32.77  | 35.70  | 0.11            | 1.31        | 400 s  | 4/4/8   |
| 120     | 1e-4   | 0.1       | 5 (50)            | Leonid          | 10.62    | 13.90  | 17.07  | 20.10  | 23.43  | 26.60  | 29.66  | 32.74  | 35.65  | 0.16            | 1.27        | 263 s  | 4/4/8   |
| 120     | 1e-4   | 0.1       | 50 (500)          | Leonid          | 10.66    | 13.99  | 17.11  | 20.15  | 23.37  | 26.58  | 29.65  | 32.75  | 35.69  | 0.12            | 1.31        | 214 s  | 4/4/8   |
| 120     | 1e-4   | 0.1       | 500 (5000)        | Leonid          | 8.89     | 12.49  | 16.00  | 19.37  | 22.81  | 26.27  | 29.50  | 32.69  | 35.69  | 1.80            | 0.72        | 207 s  | 4/4/8   |
| 120     | 5e-5   | 0.01      | 5 (100)           | Claude          | 10.71    | 14.06  | 17.16  | 20.21  | 23.50  | 26.68  | 29.71  | 32.80  | 35.83  | 0.02            | 1.33        | 829 s  | 1/1/1   |
| 120     | 1e-5   | 0.01      | 5 (500)           | Claude          | 10.69    | 14.05  | 17.14  | 20.19  | 23.49  | 26.66  | 29.69  | 32.78  | 35.81  | 0.00            | 1.32        | 4766 s | 1/1/1   |
| 120     | 1e-5   | 0.01      | 50 (5000)         | Leonid          | 10.69    | 14.05  | 17.14  | 20.19  | 23.48  | 26.66  | 29.69  | 32.78  | 35.81  | 0.01            | 1.32        | 9785 s | 4/4/8   |

## Reading the table

1. **Same case, both machines:** at 80 and 120 div with LoadSpeed 0.01 the two builds agree to 0.01 mm at every load. At 40 div one point differs by 0.03 mm (12.70 vs 12.73) and at LoadSpeed 0.1 up to 0.14 mm.
2. **Step:** at 1e-4 and below the result is converged within 0.12 mm (in Claude's runs). 2e-4 is off by up to 0.6 mm and blows up at 120 div. 4e-4 blows up everywhere.
   - **Step 2e-4 at LoadSpeed 0.05 (Leonid, 13 Nov, 80 div, window 5 ms = 25 steps):** up to 0.67 mm below the same run at 1e-4 (35.14 vs 35.81 at 4501.1 kg), like 2e-4 at LoadSpeed 0.01 (0.59 mm). 130 s against 245 s. Not converged, so keep 1e-4.
3. **LoadSpeed:** at 80 and 120 div, 0.001 to 0.02 agree within 0.01 mm; at 80 div 0.05 is within 0.02 mm (245 s on Leonid's PC); 0.1 is off by up to 0.07 mm (80) and 0.12 mm (120). At 40 div, 0.02, 0.05 and 0.1 all drop the 1358.7 kg point by about 0.6 mm (and 1812.3 kg by 0.3 mm); from 2251.1 kg on they agree within 0.03 mm.
   - **Window 500 steps (Leonid):** LoadSpeed 0.05 stays within 0.02 mm of 0.01 at 80 and 120 div, and 0.1 comes closer: within 0.06 mm (80) and 0.04 mm (120), against 0.07 and 0.12 with window 50. At 40 div the 1358.7 kg point is still 0.51 mm low (12.22 vs 12.73).
   - **Reference with a 50 ms window (Leonid, 13 Nov, 5000 steps at 1e-5):** within 0.01 mm of the 5 ms reference at every load, so the reference does not depend on the window.
   - **Window 5000 steps (0.5 s):** the first points drop by about 1.7 mm (8.86 vs 10.60 at 80 div) and 80 and 120 div give the same curve, so the window, not the model, sets those points. Too long. Its lower RMS vs data is not a better fit.
4. **Division:** 40 div is up to 1.4 mm from the reference at LoadSpeed ≤ 0.01; 60 div 0.36 mm; 80 div 0.19 mm; 120 div at 1e-4 0.12 mm.
5. **Chosen (13 Nov, replaces 12 Nov's LoadSpeed 0.02):** 80 div, step 1e-4, LoadSpeed 0.05, window 50 ms (500 steps): 0.20 mm from the reference, within 0.02 mm of LoadSpeed 0.01, 169 s on Leonid's PC.
   - **Last check (Leonid, 13 Nov):** the chosen set at step 1e-5 (window still 50 ms = 5000 steps) is within 0.01 mm of step 1e-4 at every load, and took 2451 s against 169 s. So step 1e-4 is converged for this set too.

CSV of the same table: combined_div_step_loadspeed_2026-11-12.csv

## Speed-up tests (Claude, 80 div, step 1e-4, LoadSpeed 0.01)

Deflection in mm. Simulated time to the last point, then wall time. The first four ran side by side with 1 thread each; the thread runs ran alone, one after another.

| test                                                | contact at t | zero (spindle height) | 902.9 | 1358.7 | 1812.3 | 2251.1 | 2704.5 | 3165.8 | 3614.3 | 4069.9 | 4501.1 | sim time | wall  |
|-----------------------------------------------------|--------------|-----------------------|-------|--------|--------|--------|--------|--------|--------|--------|--------|----------|-------|
| base (drop 0.1, pause 0.25), 4 side by side         | 0.757 s      | 0.50733 m             | 10.60 | 13.86  | 17.12  | 20.31  | 23.54  | 26.57  | 29.59  | 32.75  | 35.82  | 4.59 s   | 324 s |
| no pause, 4 side by side                            | 0.757 s      | 0.50733 m             | 10.60 | 13.86  | 17.12  | 20.31  | 23.54  | 26.57  | 29.59  | 32.75  | 35.82  | 4.34 s   | 308 s |
| fast drop (1 m/s, 0.1 below z 0.52), 4 side by side | 0.192 s      | 0.50712 m             | 10.39 | 13.65  | 16.91  | 20.10  | 23.33  | 26.36  | 29.38  | 32.54  | 35.61  | 4.00 s   | 284 s |
| fast drop + no pause, 4 side by side                | 0.192 s      | 0.50712 m             | 10.39 | 13.65  | 16.91  | 20.10  | 23.33  | 26.36  | 29.38  | 32.54  | 35.61  | 3.75 s   | 267 s |
| threads 1/1/1, alone                                | 0.757 s      | 0.50733 m             | 10.60 | 13.86  | 17.12  | 20.31  | 23.54  | 26.57  | 29.59  | 32.75  | 35.82  | 4.59 s   | 312 s |
| threads 2/2/2, alone                                | 0.757 s      | 0.50733 m             | 10.60 | 13.86  | 17.12  | 20.31  | 23.54  | 26.57  | 29.59  | 32.75  | 35.82  | 4.59 s   | 292 s |
| threads 4/4/8 (Leonid's), alone                     | 0.757 s      | 0.50733 m             | 10.60 | 13.86  | 17.12  | 20.31  | 23.54  | 26.57  | 29.59  | 32.75  | 35.82  | 4.59 s   | 275 s |

- **No pause:** identical results at every load (to 0.01 mm), 0.25 s less to simulate.
- **Fast drop:** contact comes 0.57 s earlier, but the zero is 0.21 mm lower, so every deflection is 0.21 mm smaller (same shape). Likely cause (inferred): the tire is still inflating when it touches the plate that early.
- **Threads:** 4 threads were only 12% faster than 1 thread. 4 single-thread runs side by side took 324 s each, so on 4 cores that gives about 3.4x more runs per hour than one 4-thread run after another (275 s each).

## LoadSpeed 0.05 checks away from the base case (Claude, 80 div, step 1e-4, window 5 ms = 50 steps)

To check that 0.05 is not only fine for the base springs: four corners of the spring range and two lower pressures, each at LoadSpeed 0.01 and 0.05. Deflection in mm. 4 single-thread runs side by side.

| case                              | LoadSpeed | 902.9 | 1358.7 | 1812.3 | 2251.1 | 2704.5 | 3165.8 | 3614.3 | 4069.9 | 4501.1 | max diff 0.05 vs 0.01 | time  |
|-----------------------------------|-----------|-------|--------|--------|--------|--------|--------|--------|--------|--------|-----------------------|-------|
| all low: kC 2e7, kT 5e5, kBC 1e3  | 0.01      | 14.32 | 18.59  | 22.69  | 26.70  | 30.68  | 34.54  | 38.36  | 42.31  | 46.13  |                       | 376 s |
|                                   | 0.05      | 14.30 | 18.60  | 22.68  | 26.68  | 30.66  | 34.52  | 38.33  | 42.27  | 46.08  | 0.05                  | 128 s |
| all high: kC 1e8, kT 5e6, kBC 1e4 | 0.01      | 8.02  | 10.35  | 12.69  | 15.01  | 17.47  | 20.05  | 22.38  | 24.62  | 26.68  |                       | 246 s |
|                                   | 0.05      | 8.01  | 10.34  | 12.69  | 15.01  | 17.47  | 20.05  | 22.37  | 24.61  | 26.65  | 0.03                  | 108 s |
| kC 2e7, kT 5e6, kBC 1e3           | 0.01      | 13.13 | 16.18  | 19.11  | 21.94  | 24.91  | 27.67  | 30.43  | 33.35  | 36.23  |                       | 311 s |
|                                   | 0.05      | 13.13 | 16.18  | 19.10  | 21.93  | 24.90  | 27.67  | 30.43  | 33.35  | 36.23  | 0.01                  | 116 s |
| kC 1e8, kT 5e5, kBC 1e4           | 0.01      | 10.69 | 14.52  | 18.35  | 22.07  | 25.94  | 29.64  | 33.14  | 36.83  | 40.39  |                       | 346 s |
|                                   | 0.05      | 10.68 | 14.50  | 18.34  | 22.07  | 25.93  | 29.61  | 33.11  | 36.79  | 40.34  | 0.05                  | 125 s |
| base springs, 700 kPa             | 0.01      | 11.51 | 15.35  | 19.25  | 23.01  | 26.63  | 30.41  | 34.19  | 38.15  | 41.73  |                       | 353 s |
|                                   | 0.05      | 11.50 | 15.37  | 19.25  | 22.99  | 26.62  | 30.40  | 34.19  | 38.15  | 41.72  | 0.02                  | 130 s |
| base springs, 600 kPa             | 0.01      | 12.19 | 16.45  | 20.82  | 24.83  | 28.97  | 33.29  | 37.63  | 41.86  | 45.54  |                       | 381 s |
|                                   | 0.05      | 12.18 | 16.44  | 20.80  | 24.82  | 28.96  | 33.28  | 37.62  | 41.85  | 45.52  | 0.02                  | 135 s |

- In all six cases 0.05 is within 0.05 mm of 0.01 at every load and 2.3 to 2.9 times faster. The largest gaps (0.05 mm) are in the two cases with soft transversal springs (kT 5e5), at the last loads.

## Final set on the corner cases (Claude, 13 Nov)

Final set = step 1e-4, LoadSpeed 0.05, window 50 ms (500 steps). Compared with LoadSpeed 0.01 (window 5 ms) at 80 div, and at 120 div for the two extreme corners. Deflection in mm, 1 thread per run, 4 runs side by side.

| case                              | run                                            | 902.9 | 1358.7 | 1812.3 | 2251.1 | 2704.5 | 3165.8 | 3614.3 | 4069.9 | 4501.1 | max diff        | time  |
|-----------------------------------|------------------------------------------------|-------|--------|--------|--------|--------|--------|--------|--------|--------|-----------------|-------|
| all low: kC 2e7, kT 5e5, kBC 1e3  | 80 div, LS 0.01, 5 ms                          | 14.32 | 18.59  | 22.69  | 26.70  | 30.68  | 34.54  | 38.36  | 42.31  | 46.13  |                 | 376 s |
|                                   | 80 div, final set                              | 14.28 | 18.58  | 22.68  | 26.68  | 30.66  | 34.52  | 38.33  | 42.27  | 46.08  | 0.05 vs LS 0.01 | 147 s |
|                                   | 120 div, final set                             | 14.36 | 18.70  | 22.67  | 26.58  | 30.59  | 34.48  | 38.32  | 42.34  | 46.02  | 0.12 vs 80 div  | 214 s |
| all high: kC 1e8, kT 5e6, kBC 1e4 | 80 div, LS 0.01, 5 ms                          | 8.02  | 10.35  | 12.69  | 15.01  | 17.47  | 20.05  | 22.38  | 24.62  | 26.68  |                 | 246 s |
|                                   | 80 div, final set                              | 8.00  | 10.34  | 12.69  | 15.01  | 17.47  | 20.03  | 22.36  | 24.60  | 26.67  | 0.02 vs LS 0.01 | 128 s |
|                                   | 80 div, final set, Leonid's PC (4/4/8 threads) | 8.00  | 10.34  | 12.69  | 15.01  | 17.47  | 20.03  | 22.36  | 24.60  | 26.67  | 0.00 vs Claude  | 185 s |
|                                   | 120 div, final set                             | 8.01  | 10.47  | 12.80  | 15.09  | 17.48  | 19.72  | 21.97  | 24.38  | 26.75  | 0.39 vs 80 div  | 179 s |
| kC 2e7, kT 5e6, kBC 1e3           | 80 div, LS 0.01, 5 ms                          | 13.13 | 16.18  | 19.11  | 21.94  | 24.91  | 27.67  | 30.43  | 33.35  | 36.23  |                 | 311 s |
|                                   | 80 div, final set                              | 13.10 | 16.18  | 19.10  | 21.94  | 24.88  | 27.67  | 30.43  | 33.35  | 36.23  | 0.03 vs LS 0.01 | 134 s |
| kC 1e8, kT 5e5, kBC 1e4           | 80 div, LS 0.01, 5 ms                          | 10.69 | 14.52  | 18.35  | 22.07  | 25.94  | 29.64  | 33.14  | 36.83  | 40.39  |                 | 346 s |
|                                   | 80 div, final set                              | 10.66 | 14.50  | 18.35  | 22.07  | 25.92  | 29.61  | 33.12  | 36.79  | 40.34  | 0.05 vs LS 0.01 | 150 s |
| base springs, 700 kPa             | 80 div, LS 0.01, 5 ms                          | 11.51 | 15.35  | 19.25  | 23.01  | 26.63  | 30.41  | 34.19  | 38.15  | 41.73  |                 | 353 s |
|                                   | 80 div, final set                              | 11.51 | 15.35  | 19.25  | 22.99  | 26.62  | 30.40  | 34.19  | 38.15  | 41.71  | 0.02 vs LS 0.01 | 144 s |
| base springs, 600 kPa             | 80 div, LS 0.01, 5 ms                          | 12.19 | 16.45  | 20.82  | 24.83  | 28.97  | 33.29  | 37.63  | 41.86  | 45.54  |                 | 381 s |
|                                   | 80 div, final set                              | 12.18 | 16.45  | 20.81  | 24.82  | 28.96  | 33.29  | 37.62  | 41.85  | 45.53  | 0.01 vs LS 0.01 | 150 s |

- **Same case on both machines:** Leonid's PC gives the same all-high numbers as Claude's build at every load (to 0.01 mm).
- **Final set vs LoadSpeed 0.01:** within 0.05 mm in all six cases, so the speed-up holds over the whole spring range and at 600/700 kPa.
- **80 vs 120 div:** all-low corner within 0.12 mm; all-high corner up to 0.39 mm (21.97 vs 22.36 at 3614.3 kg, 80 div deflects more). At the base springs it is 0.19 mm. The difference changes sign along the curve, so it is not a constant shift; likely mesh steps as nodes come into contact, worse for the stiff tire with its short contact patch (inferred).

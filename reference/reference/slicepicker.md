+++
title = "slicepicker"
+++

## slicepicker, tile type

The `slicepicker` is an interactive tile that offers navigation controls to pick a slice.

![Image](/images/ref_slicepicker.png)

In this example, the slice picker controls the ballistic trajectory of a projectile subjected to gravity and wind.

```envision
table Angles[angle] = with
  [| as Angle |]
  [| 85       |]
  [| 75       |]
  [| 60       |]
  [| 45       |]
  [| 30       |]
  [| 15       |]
  [|  5       |]
 
table Velocity = with
  [| as Velocity |]
  [| 100 |]
  [|  90 |]
  [|  80 |]
  [|  60 |]
  [|  40 |]
  [|  20 |]
 
table Wind = with
  [| -4 as Wind |]
  [| -2 |]
  [| -1 |]
  [| 0 |]
  [| 1 |]
  [| 2 |]
  [| 4 |]
 
table AngleVelocity = cross(Angles, Velocity)
table AngleVelocity = where AngleVelocity.*
 
table Parameters = cross(AngleVelocity, Wind)
table Parameters[p] = where Parameters.*
 
Parameters.Angle = Angles.Angle into AngleVelocity
Parameters.Velocity = Velocity.Velocity into AngleVelocity
Parameters.Wind = Wind.Wind
 
table Time = extend.range(500)
table Trajectory = cross(Time, Parameters)
 
const dt = 0.1
 
def process simulate(wind: number; ivx: number, ivy: number) with
  keep x = 0
  keep y = 0
  keep vx = ivx
  keep vy = ivy
  // Return current value
  ix = x
  iy = y
  // Do not allow traversing the ground
  where y + vy*dt <= 0
    vx = -(y/dt/vy) * vx
    vy = -y/dt
  // Integrate 1st order
  x = x + vx * dt
  y = y + vy * dt
  // Integrate 2nd order
  vx = vx + wind * dt
  vy = vy - 9.82 * dt
  return (ix, iy)
 
Parameters.VelX = cos(Parameters.Angle * 0.0174533) * Parameters.Velocity
Parameters.VelY = sin(Parameters.Angle * 0.0174533) * Parameters.Velocity
 
Trajectory.X, Trajectory.Y = simulate(Parameters.Wind; Parameters.VelX, Parameters.VelY)
  by p scan (Time.N into Trajectory)
 
table Slices[slice] = slice by p title:""
Trajectory.slice = Parameters.slice
 
show slicepicker "Ballistic parameters" a1b4 with
  same(Parameters.Angle) as "Angle"
  same(Parameters.Velocity) as "Velocity"
  same(Parameters.Wind) as "Wind"
 
show table "Trajectory" a5b7 slices:Trajectory.slice with
  Trajectory.X
  Trajectory.Y
 
maxy = max(Trajectory.Y) * 1.1
maxx = max(Trajectory.X) * 1.1
 
show scatter "Trajectory" c1f7 slices:Trajectory.slice {
  vaxis { axisMax: #(maxy) }
  haxis { axisMax: #(maxx) }
} with
  Trajectory.X
  Trajectory.Y
  order by Time.N
```

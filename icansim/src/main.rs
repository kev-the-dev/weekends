use std::time::{Duration, Instant};
use std::thread::sleep;

struct SimulationState {
    startTime: Instant,
    time: Instant,
}

impl Default for SimulationState {
    fn default() -> Self { 
        let now = Instant::now();
        Self{startTime: now, time: now} 
    }
}

trait Entity
{
    fn update(&mut self, state: &SimulationState);
}

struct ExampleEntity;

impl Entity for ExampleEntity
{
    fn update(&mut self, state: &SimulationState)
    {
        let elapsed = state.time - state.startTime;
        println!("Time is {:?}", elapsed);
    }
}

#[derive(Default)]
struct Simulation
{
    entities: Vec<Box<dyn Entity>>,
    state: SimulationState,
}

impl Simulation
{
    fn update(&mut self, elapsed_time: Duration)
    {
        for entitity in &mut self.entities
        {
            entitity.update(&self.state);
        }
        self.state.time += elapsed_time;
    }
    fn run_for(&mut self, duration: Duration, update_hz: f64)
    {
        // TODO: actually use update_hz
        let update_period = Duration::from_millis(10);
        let sim_end_time = self.state.time + duration;
        let mut real_time = Instant::now();
        let mut real_time_goal = real_time;
        while self.state.time < sim_end_time
        {
            self.update(update_period);
            real_time_goal += update_period;
            real_time = Instant::now();
            if real_time < real_time_goal
            {
                let sleep_time = real_time_goal - real_time;
                std::thread::sleep(sleep_time);
            }
        }
    }
}


fn main() {
    let mut my_sim: Simulation = Default::default();
    my_sim.entities.push(Box::new(ExampleEntity{}));
    my_sim.run_for(Duration::from_secs(5), 100f64);
    println!("Hello, world!");
}

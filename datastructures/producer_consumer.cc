#include <iostream>
#include <mutex>
#include <condition_variable>
#include <thread>
#include <queue>
#include <functional>


class ProducerConsumerExample
{
public:
    ProducerConsumerExample();
    void run();
private:
    void producer_thread();
    void consumer_thread();
    std::mutex mutex;
    std::condition_variable cv;
    std::queue<std::string> queue;
};

ProducerConsumerExample::ProducerConsumerExample()
{
}

void ProducerConsumerExample::run()
{
    auto producer_thread = std::thread(std::bind(&ProducerConsumerExample::producer_thread, this));
    consumer_thread();  

    producer_thread.join();
}

void ProducerConsumerExample::producer_thread()
{
    for (size_t i = 0; i < 100; ++i)
    {
        std::string message = "Data " + std::to_string(i + 1);
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        {
            std::unique_lock<std::mutex> l(mutex);
            queue.push(message);
        }
        std::cout << "Produced " << message << std::endl;
        cv.notify_one();
    }
}

void ProducerConsumerExample::consumer_thread()
{
    for (size_t i = 0; i < 100; ++i)
    {
        std::unique_lock<std::mutex> l(mutex);
        cv.wait(l, [this](){ return !this->queue.empty();});
        std::string message = queue.front();
        queue.pop();
        std::cout << "Consumed " << message << std::endl;
    }
}


int main()
{
    ProducerConsumerExample node;
    node.run();
    return 0;
}

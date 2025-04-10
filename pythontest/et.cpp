#include <uhd/usrp/multi_usrp.hpp>
#include <uhd/stream.hpp>
#include <uhd/utils/thread.hpp>
#include <iostream>
#include <vector>
#include <complex>
#include <csignal>

static bool stop_signal_called = false;

void signal_handler(int) {
    stop_signal_called = true;
}

int main(int argc, char* argv[]) {
    try {
        // Set up signal handler for clean exit
        std::signal(SIGINT, signal_handler);

        // Create a USRP device
        std::cout << "Creating the USRP device..." << std::endl;
        auto usrp = uhd::usrp::multi_usrp::make("type=b200");

        // Set the sample rate
        double sample_rate = 1e6; // 1 MS/s
        std::cout << "Setting sample rate to " << sample_rate / 1e6 << " MS/s..." << std::endl;
        usrp->set_rx_rate(sample_rate);

        // Set the center frequency
        double freq = 2.4e9; // 2.4 GHz
        std::cout << "Setting center frequency to " << freq / 1e9 << " GHz..." << std::endl;
        usrp->set_rx_freq(freq);

        // Set the gain
        double gain = 30.0; // 30 dB
        std::cout << "Setting gain to " << gain << " dB..." << std::endl;
        usrp->set_rx_gain(gain);

        // Create a receive streamer
        uhd::stream_args_t stream_args("fc32"); // Complex float32
        auto rx_stream = usrp->get_rx_stream(stream_args);

        // Allocate buffer for samples
        size_t num_samples = rx_stream->get_max_num_samps();
        std::vector<std::complex<float>> buffer(num_samples);

        // Stream command
        uhd::stream_cmd_t stream_cmd(uhd::stream_cmd_t::STREAM_MODE_START_CONTINUOUS);
        stream_cmd.stream_now = true;
        rx_stream->issue_stream_cmd(stream_cmd);

        std::cout << "Receiving samples..." << std::endl;

        // Receive loop
        while (!stop_signal_called) {
            size_t num_rx_samps = rx_stream->recv(&buffer.front(), buffer.size(), uhd::rx_metadata_t(), 1.0);
            std::cout << "Received " << num_rx_samps << " samples" << std::endl;
        }

        // Stop streaming
        stream_cmd.stream_mode = uhd::stream_cmd_t::STREAM_MODE_STOP_CONTINUOUS;
        rx_stream->issue_stream_cmd(stream_cmd);

        std::cout << "Done!" << std::endl;
    } catch (const uhd::exception& e) {
        std::cerr << "UHD Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
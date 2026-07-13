// Fragmentation scenario network design
import inet.node.inet.StandardHost;
import inet.node.inet.Router;
import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import ned.DatarateChannel;

network FragmentationNetwork
{
    types:
        channel C extends DatarateChannel {
            datarate = 100Mbps;
            delay = 0.1us;
        }
    submodules:
        configurator: Ipv4NetworkConfigurator; // Assigns IP addresses automatically
        hostA: StandardHost;
        router: Router;
        hostB: StandardHost;
    connections:
        // Connecting Host A to Router (Port 0)
        hostA.ethg++ <--> C <--> router.ethg++;
        // Connecting Router to Host B (Port 1)
        router.ethg++ <--> C <--> hostB.ethg++;
}


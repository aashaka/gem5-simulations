from m5.objects import Cache
# Cache has the object BaseCache


# Define L1 cache
class L1Cache(Cache):

    # Define parameters which have no default value in BaseCache
    assoc=2
    hit_latency=2
    response_latency=2
    mshrs=4
    tgts_per_mshr=20

    # Don't connect to CPU side port yet, as the CPU ports are different for I and D cache
    def connectCPU(self,cpu):
        raise NotImplementedError

    # Connect L1 cache port to bus, with bus as the slave
    def connectBus(self,bus):
        self.mem_side = bus.slave


# Make instruction cache
class L1ICache(L1Cache):

    # Set size of instruction cache
    size = '16kB'

    # Connect instruction cache's port to CPU side icache port
    def connectCPU(self,cpu):
        self.cpu_side=cpu.icache_port


# Make data cache
class L1DCache(L1Cache):
    
    # Set size of data cache
    size = '64kB'

    # Connect data cache's port to CPU side dcache port
    def connectCPU(self,cpu):
        self.cpu_side=cpu.dcache_port


# Make L2 cache
class L2Cache(Cache):

    # Set non-default parameters
    size='256kB'
    assoc=8
    hit_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    # Connect to CPU side bus
    def connectCPUSideBus(self,bus):
        self.cpu_side=bus.master

    # Connect to memory side bus
    def connectMemSideBus(self,bus):
        self.mem_side=bus.slave


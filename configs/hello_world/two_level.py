import m5
from m5.objects import *
from caches import *

# Make the system
system = System()

# Set its clock frequency and voltage
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Use timing mode for memory simulation
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# Create CPU model. This one executes each instruction in a single clock cycle. (Except memory instr.)
system.cpu = TimingSimpleCPU()

# Create system-wide memory bus(Cross bar)
system.membus = SystemXBar()

# Create L1 I and D caches
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()

# Connect both L1 caches to CPU
# connectCPU(self,cpu) function has been defined in caches.py
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

#Create an L2 bus to which both L1 caches connect on CPU side and L2 cache connects on mem side
system.l2bus = L2XBar()

# Connect both L1 caches mem side port to L2 bus
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# Create an L2 cache, and connect it on cpu side with L2 bus and on mem side with system bus
system.l2cache = L2Cache()
system.l2cache.connectCPUSideBus(system.l2bus)
system.l2cache.connectMemSideBus(system.membus)

# Connect interrupt ports to membus. This is need in x86 ISA, not others
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

system.system_port = system.membus.slave

# Connect memory controller (DDR3 here) to membus
system.mem_ctrl = DDR3_1600_x64()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# Create process to run the hello world program
process = LiveProcess()
process.cmd = ['tests/test-progs/hello/bin/x86/linux/hello']
system.cpu.workload = process
system.cpu.createThreads()

# Instantiate oython class
root = Root(full_system = False, system = system)
m5.instantiate()

# Run simulation
print "Simulation starting in 3..2..1.."
exit_event = m5.simulate()

# Simulation finished
print 'Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause())


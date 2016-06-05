import m5
from m5.objects import *

# Make the system
system = System()

# Set its clock frequency and voltage
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Use timing mode for mmeory simulation
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# Create CPU model. This one executes each instruction in a single clock cycle. (Except memory instr.)
system.cpu = TimingSimpleCPU()

# Create system-wide memory bus
system.membus = SystemXBar()

# Connect cache ports on CPU to system bus. (Our system doesn't have caches)
system.cpu.icache_port = system.membus.slave
system.cpu.dcache_port = system.membus.slave

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


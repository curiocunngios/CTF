> What CPU architecture are you running on? (x86_64 I assume?)

yes most likely x86_64 but I am not 100% sure, how can I check tho? ALso why do you need to know this?

the entire `dmesg`:
```
[    0.000000] Linux version 5.4.0 (kali@pwncollege) (gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.045
[    0.000000] Command line: console=ttyS0 nokaslr
[    0.000000] x86/fpu: x87 FPU will use FXSAVE
[    0.000000] BIOS-provided physical RAM map:
[    0.000000] BIOS-e820: [mem 0x0000000000000000-0x000000000009fbff] usable
[    0.000000] BIOS-e820: [mem 0x000000000009fc00-0x000000000009ffff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000000f0000-0x00000000000fffff] reserved
[    0.000000] BIOS-e820: [mem 0x0000000000100000-0x0000000007fdffff] usable
[    0.000000] BIOS-e820: [mem 0x0000000007fe0000-0x0000000007ffffff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000fffc0000-0x00000000ffffffff] reserved
[    0.000000] NX (Execute Disable) protection: active
[    0.000000] SMBIOS 2.8 present.
[    0.000000] DMI: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.13.0-1ubuntu1.1 04/01/2014
[    0.000000] tsc: Fast TSC calibration using PIT
[    0.000000] tsc: Detected 2591.973 MHz processor
[    0.004674] e820: update [mem 0x00000000-0x00000fff] usable ==> reserved
[    0.004804] e820: remove [mem 0x000a0000-0x000fffff] usable
[    0.004916] last_pfn = 0x7fe0 max_arch_pfn = 0x400000000
[    0.005124] MTRR default type: write-back
[    0.005139] MTRR fixed ranges enabled:
[    0.005241]   00000-9FFFF write-back
[    0.005253]   A0000-BFFFF uncachable
[    0.005262]   C0000-FFFFF write-protect
[    0.005270] MTRR variable ranges enabled:
[    0.005357]   0 base 0080000000 mask FF80000000 uncachable
[    0.005372]   1 disabled
[    0.005374]   2 disabled
[    0.005375]   3 disabled
[    0.005377]   4 disabled
[    0.005378]   5 disabled
[    0.005379]   6 disabled
[    0.005380]   7 disabled
[    0.005599] x86/PAT: Configuration [0-7]: WB  WC  UC- UC  WB  WP  UC- WT  
[    0.012003] found SMP MP-table at [mem 0x000f5c90-0x000f5c9f]
[    0.013205] check: Scanning 1 areas for low memory corruption
[    0.013991] BRK [0x02c01000, 0x02c01fff] PGTABLE
[    0.014104] BRK [0x02c02000, 0x02c02fff] PGTABLE
[    0.014157] BRK [0x02c03000, 0x02c03fff] PGTABLE
[    0.015424] BRK [0x02c04000, 0x02c04fff] PGTABLE
[    0.023319] RAMDISK: [mem 0x07e1f000-0x07fdffff]
[    0.023722] ACPI: Early table checksum verification disabled
[    0.023959] ACPI: RSDP 0x00000000000F5AC0 000014 (v00 BOCHS )
[    0.024117] ACPI: RSDT 0x0000000007FE156F 000030 (v01 BOCHS  BXPCRSDT 00000001 BXPC 00000001)
[    0.024531] ACPI: FACP 0x0000000007FE144B 000074 (v01 BOCHS  BXPCFACP 00000001 BXPC 00000001)
[    0.024929] ACPI: DSDT 0x0000000007FE0040 00140B (v01 BOCHS  BXPCDSDT 00000001 BXPC 00000001)
[    0.024978] ACPI: FACS 0x0000000007FE0000 000040
[    0.025012] ACPI: APIC 0x0000000007FE14BF 000078 (v01 BOCHS  BXPCAPIC 00000001 BXPC 00000001)
[    0.025025] ACPI: HPET 0x0000000007FE1537 000038 (v01 BOCHS  BXPCHPET 00000001 BXPC 00000001)
[    0.025376] ACPI: Local APIC address 0xfee00000
[    0.026308] No NUMA configuration found
[    0.026352] Faking a node at [mem 0x0000000000000000-0x0000000007fdffff]
[    0.026825] NODE_DATA(0) allocated [mem 0x07e1b000-0x07e1efff]
[    0.035721] Zone ranges:
[    0.035806]   DMA      [mem 0x0000000000001000-0x0000000000ffffff]
[    0.035838]   DMA32    [mem 0x0000000001000000-0x0000000007fdffff]
[    0.035844]   Normal   empty
[    0.035855] Movable zone start for each node
[    0.035877] Early memory node ranges
[    0.035899]   node   0: [mem 0x0000000000001000-0x000000000009efff]
[    0.035981]   node   0: [mem 0x0000000000100000-0x0000000007fdffff]
[    0.043382] Zeroed struct page in unavailable ranges: 98 pages
[    0.043510] Initmem setup node 0 [mem 0x0000000000001000-0x0000000007fdffff]
[    0.043633] On node 0 totalpages: 32638
[    0.043715]   DMA zone: 64 pages used for memmap
[    0.043731]   DMA zone: 21 pages reserved
[    0.043767]   DMA zone: 3998 pages, LIFO batch:0
[    0.044194]   DMA32 zone: 448 pages used for memmap
[    0.044213]   DMA32 zone: 28640 pages, LIFO batch:7
[    0.045964] ACPI: PM-Timer IO Port: 0x608
[    0.045992] ACPI: Local APIC address 0xfee00000
[    0.048459] ACPI: LAPIC_NMI (acpi_id[0xff] dfl dfl lint[0x1])
[    0.048757] IOAPIC[0]: apic_id 0, version 32, address 0xfec00000, GSI 0-23
[    0.048842] ACPI: INT_SRC_OVR (bus 0 bus_irq 0 global_irq 2 dfl dfl)
[    0.049051] ACPI: INT_SRC_OVR (bus 0 bus_irq 5 global_irq 5 high level)
[    0.049075] ACPI: INT_SRC_OVR (bus 0 bus_irq 9 global_irq 9 high level)
[    0.049142] ACPI: INT_SRC_OVR (bus 0 bus_irq 10 global_irq 10 high level)
[    0.049148] ACPI: INT_SRC_OVR (bus 0 bus_irq 11 global_irq 11 high level)
[    0.049201] ACPI: IRQ0 used by override.
[    0.049236] ACPI: IRQ5 used by override.
[    0.049239] ACPI: IRQ9 used by override.
[    0.049240] ACPI: IRQ10 used by override.
[    0.049242] ACPI: IRQ11 used by override.
[    0.049283] Using ACPI (MADT) for SMP configuration information
[    0.049314] ACPI: HPET id: 0x8086a201 base: 0xfed00000
[    0.057618] smpboot: Allowing 1 CPUs, 0 hotplug CPUs
[    0.058181] PM: Registered nosave memory: [mem 0x00000000-0x00000fff]
[    0.058209] PM: Registered nosave memory: [mem 0x0009f000-0x0009ffff]
[    0.058228] PM: Registered nosave memory: [mem 0x000a0000-0x000effff]
[    0.058231] PM: Registered nosave memory: [mem 0x000f0000-0x000fffff]
[    0.058309] [mem 0x08000000-0xfffbffff] available for PCI devices
[    0.058610] clocksource: refined-jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 1s
[    0.557739] setup_percpu: NR_CPUS:64 nr_cpumask_bits:64 nr_cpu_ids:1 nr_node_ids:1
[    0.570203] percpu: Embedded 50 pages/cpu s167064 r8192 d29544 u2097152
[    0.570510] pcpu-alloc: s167064 r8192 d29544 u2097152 alloc=1*2097152
[    0.570588] pcpu-alloc: [0] 0 
[    0.571983] Built 1 zonelists, mobility grouping on.  Total pages: 32105
[    0.571999] Policy zone: DMA32
[    0.572114] Kernel command line: console=ttyS0 nokaslr
[    0.572952] Dentry cache hash table entries: 16384 (order: 5, 131072 bytes, linear)
[    0.573105] Inode-cache hash table entries: 8192 (order: 4, 65536 bytes, linear)
[    0.573959] mem auto-init: stack:off, heap alloc:off, heap free:off
[    0.574140] Calgary: detecting Calgary via BIOS EBDA area
[    0.574165] Calgary: Unable to locate Rio Grande table in EBDA - bailing!
[    0.576048] Memory: 97444K/130552K available (14340K kernel code, 1350K rwdata, 3288K rodata, 132)
[    0.587400] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=1, Nodes=1
[    0.600557] rcu: Hierarchical RCU implementation.
[    0.600575] rcu: 	RCU event tracing is enabled.
[    0.600595] rcu: 	RCU restricting CPUs from NR_CPUS=64 to nr_cpu_ids=1.
[    0.600684] rcu: RCU calculated value of scheduler-enlistment delay is 100 jiffies.
[    0.600703] rcu: Adjusting geometry for rcu_fanout_leaf=16, nr_cpu_ids=1
[    0.602097] NR_IRQS: 4352, nr_irqs: 256, preallocated irqs: 16
[    0.607462] random: get_random_bytes called from start_kernel+0x30e/0x4db with crng_init=0
[    0.618783] Console: colour VGA+ 80x25
[    0.630334] printk: console [ttyS0] enabled
[    0.630951] ACPI: Core revision 20190816
[    0.634176] clocksource: hpet: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604467 s
[    0.637272] APIC: Switch to symmetric I/O mode setup
[    0.640599] ..TIMER: vector=0x30 apic1=0 pin1=2 apic2=-1 pin2=-1
[    0.645782] clocksource: tsc-early: mask: 0xffffffffffffffff max_cycles: 0x255c9d3d01a, max_idle_s
[    0.646585] Calibrating delay loop (skipped), value calculated using timer frequency.. 5183.94 Bo)
[    0.647058] pid_max: default: 32768 minimum: 301
[    0.647821] LSM: Security Framework initializing
[    0.648432] SELinux:  Initializing.
[    0.648938] Mount-cache hash table entries: 512 (order: 0, 4096 bytes, linear)
[    0.649482] Mountpoint-cache hash table entries: 512 (order: 0, 4096 bytes, linear)
[    0.661904] Last level iTLB entries: 4KB 0, 2MB 0, 4MB 0
[    0.662162] Last level dTLB entries: 4KB 0, 2MB 0, 4MB 0, 1GB 0
[    0.662567] Spectre V1 : Mitigation: usercopy/swapgs barriers and __user pointer sanitization
[    0.662782] Spectre V2 : Mitigation: Full AMD retpoline
[    0.662852] Spectre V2 : Spectre v2 / SpectreRSB mitigation: Filling RSB on context switch
[    0.663000] Speculative Store Bypass: Vulnerable
[    0.811027] Freeing SMP alternatives memory: 40K
[    0.892590] random: fast init done
[    0.917443] smpboot: CPU0: AMD QEMU Virtual CPU version 2.5+ (family: 0x6, model: 0x6, stepping: )
[    0.920832] Performance Events: PMU not available due to virtualization, using software events on.
[    0.922827] rcu: Hierarchical SRCU implementation.
[    0.926376] Huh? What family is it: 0x6?!
[    0.927161] smp: Bringing up secondary CPUs ...
[    0.927696] smp: Brought up 1 node, 1 CPU
[    0.927914] smpboot: Max logical packages: 1
[    0.928005] smpboot: Total of 1 processors activated (5183.94 BogoMIPS)
[    0.935546] devtmpfs: initialized
[    0.940264] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 191126044s
[    0.940544] futex hash table entries: 256 (order: 2, 16384 bytes, linear)
[    0.943705] PM: RTC time: 06:54:39, date: 2025-06-27
[    0.947235] NET: Registered protocol family 16
[    0.949611] audit: initializing netlink subsys (disabled)
[    0.953443] cpuidle: using governor menu
[    0.954688] audit: type=2000 audit(1751007279.315:1): state=initialized audit_enabled=0 res=1
[    0.956213] ACPI: bus type PCI registered
[    0.958125] PCI: Using configuration type 1 for base access
[    0.974749] HugeTLB registered 2.00 MiB page size, pre-allocated 0 pages
[    0.976604] cryptomgr_test (19) used greatest stack depth: 15520 bytes left
[    0.980387] kworker/u2:0 (21) used greatest stack depth: 14632 bytes left
[    0.982768] kworker/u2:0 (26) used greatest stack depth: 14168 bytes left
[    0.989796] ACPI: Added _OSI(Module Device)
[    0.989960] ACPI: Added _OSI(Processor Device)
[    0.990018] ACPI: Added _OSI(3.0 _SCP Extensions)
[    0.990076] ACPI: Added _OSI(Processor Aggregator Device)
[    0.990202] ACPI: Added _OSI(Linux-Dell-Video)
[    0.990262] ACPI: Added _OSI(Linux-Lenovo-NV-HDMI-Audio)
[    0.990329] ACPI: Added _OSI(Linux-HPI-Hybrid-Graphics)
[    1.000176] ACPI: 1 ACPI AML tables successfully acquired and loaded
[    1.009896] ACPI: Interpreter enabled
[    1.011020] ACPI: (supports S0 S3 S4 S5)
[    1.011186] ACPI: Using IOAPIC for interrupt routing
[    1.011716] PCI: Using host bridge windows from ACPI; if necessary, use "pci=nocrs" and report a g
[    1.012663] ACPI: Enabled 2 GPEs in block 00 to 0F
[    1.036631] ACPI: PCI Root Bridge [PCI0] (domain 0000 [bus 00-ff])
[    1.037213] acpi PNP0A03:00: _OSC: OS supports [ASPM ClockPM Segments MSI HPX-Type3]
[    1.037443] acpi PNP0A03:00: fail to add MMCONFIG information, can't access extended PCI configur.
[    1.039815] PCI host bridge to bus 0000:00
[    1.040118] pci_bus 0000:00: root bus resource [io  0x0000-0x0cf7 window]
[    1.040474] pci_bus 0000:00: root bus resource [io  0x0d00-0xffff window]
[    1.040686] pci_bus 0000:00: root bus resource [mem 0x000a0000-0x000bffff window]
[    1.040779] pci_bus 0000:00: root bus resource [mem 0x08000000-0xfebfffff window]
[    1.040872] pci_bus 0000:00: root bus resource [mem 0x100000000-0x17fffffff window]
[    1.041028] pci_bus 0000:00: root bus resource [bus 00-ff]
[    1.042684] pci 0000:00:00.0: [8086:1237] type 00 class 0x060000
[    1.045817] pci 0000:00:01.0: [8086:7000] type 00 class 0x060100
[    1.046535] pci 0000:00:01.1: [8086:7010] type 00 class 0x010180
[    1.049204] pci 0000:00:01.1: reg 0x20: [io  0xc080-0xc08f]
[    1.049867] pci 0000:00:01.1: legacy IDE quirk: reg 0x10: [io  0x01f0-0x01f7]
[    1.050493] pci 0000:00:01.1: legacy IDE quirk: reg 0x14: [io  0x03f6]
[    1.050676] pci 0000:00:01.1: legacy IDE quirk: reg 0x18: [io  0x0170-0x0177]
[    1.050807] pci 0000:00:01.1: legacy IDE quirk: reg 0x1c: [io  0x0376]
[    1.051954] pci 0000:00:01.3: [8086:7113] type 00 class 0x068000
[    1.052443] pci 0000:00:01.3: quirk: [io  0x0600-0x063f] claimed by PIIX4 ACPI
[    1.052488] pci 0000:00:01.3: quirk: [io  0x0700-0x070f] claimed by PIIX4 SMB
[    1.053953] pci 0000:00:02.0: [1234:1111] type 00 class 0x030000
[    1.054443] pci 0000:00:02.0: reg 0x10: [mem 0xfd000000-0xfdffffff pref]
[    1.055443] pci 0000:00:02.0: reg 0x18: [mem 0xfebb0000-0xfebb0fff]
[    1.056915] pci 0000:00:02.0: reg 0x30: [mem 0xfeba0000-0xfebaffff pref]
[    1.058399] pci 0000:00:03.0: [8086:100e] type 00 class 0x020000
[    1.059827] pci 0000:00:03.0: reg 0x10: [mem 0xfeb80000-0xfeb9ffff]
[    1.060737] pci 0000:00:03.0: reg 0x14: [io  0xc000-0xc03f]
[    1.061443] pci 0000:00:03.0: reg 0x30: [mem 0xfeb00000-0xfeb7ffff pref]
[    1.062327] pci 0000:00:04.0: [1af4:1009] type 00 class 0x000200
[    1.062842] pci 0000:00:04.0: reg 0x10: [io  0xc040-0xc07f]
[    1.063443] pci 0000:00:04.0: reg 0x14: [mem 0xfebb1000-0xfebb1fff]
[    1.064915] pci 0000:00:04.0: reg 0x20: [mem 0xfe000000-0xfe003fff 64bit pref]
[    1.069443] ACPI: PCI Interrupt Link [LNKA] (IRQs 5 *10 11)
[    1.070480] ACPI: PCI Interrupt Link [LNKB] (IRQs 5 *10 11)
[    1.071036] ACPI: PCI Interrupt Link [LNKC] (IRQs 5 10 *11)
[    1.071443] ACPI: PCI Interrupt Link [LNKD] (IRQs 5 10 *11)
[    1.071558] ACPI: PCI Interrupt Link [LNKS] (IRQs *9)
[    1.073215] iommu: Default domain type: Translated 
[    1.075836] pci 0000:00:02.0: vgaarb: setting as boot VGA device
[    1.076195] pci 0000:00:02.0: vgaarb: VGA device added: decodes=io+mem,owns=io+mem,locks=none
[    1.076473] pci 0000:00:02.0: vgaarb: bridge control possible
[    1.076723] vgaarb: loaded
[    1.077783] SCSI subsystem initialized
[    1.078400] libata version 3.00 loaded.
[    1.078661] ACPI: bus type USB registered
[    1.079552] usbcore: registered new interface driver usbfs
[    1.079940] usbcore: registered new interface driver hub
[    1.080344] usbcore: registered new device driver usb
[    1.080707] pps_core: LinuxPPS API ver. 1 registered
[    1.081037] pps_core: Software ver. 5.3.6 - Copyright 2005-2007 Rodolfo Giometti <giometti@linux.>
[    1.081527] PTP clock support registered
[    1.082612] EDAC MC: Ver: 3.0.0
[    1.083443] Advanced Linux Sound Architecture Driver Initialized.
[    1.084501] PCI: Using ACPI for IRQ routing
[    1.084646] PCI: pci_cache_line_size set to 64 bytes
[    1.084898] e820: reserve RAM buffer [mem 0x0009fc00-0x0009ffff]
[    1.085005] e820: reserve RAM buffer [mem 0x07fe0000-0x07ffffff]
[    1.089886] NetLabel: Initializing
[    1.089963] NetLabel:  domain hash size = 128
[    1.090024] NetLabel:  protocols = UNLABELED CIPSOv4 CALIPSO
[    1.090488] NetLabel:  unlabeled traffic allowed by default
[    1.091365] hpet: 3 channels of 0 reserved for per-cpu timers
[    1.091651] hpet0: at MMIO 0xfed00000, IRQs 2, 8, 0
[    1.092472] hpet0: 3 comparators, 64-bit 100.000000 MHz counter
[    1.098023] clocksource: Switched to clocksource tsc-early
[    1.387123] VFS: Disk quotas dquot_6.6.0
[    1.387552] VFS: Dquot-cache hash table entries: 512 (order 0, 4096 bytes)
[    1.389914] pnp: PnP ACPI init
[    1.391875] pnp 00:00: Plug and Play ACPI device, IDs PNP0b00 (active)
[    1.392345] pnp 00:01: Plug and Play ACPI device, IDs PNP0303 (active)
[    1.392530] pnp 00:02: Plug and Play ACPI device, IDs PNP0f13 (active)
[    1.392720] pnp 00:03: [dma 2]
[    1.392886] pnp 00:03: Plug and Play ACPI device, IDs PNP0700 (active)
[    1.393247] pnp 00:04: Plug and Play ACPI device, IDs PNP0400 (active)
[    1.393483] pnp 00:05: Plug and Play ACPI device, IDs PNP0501 (active)
[    1.394570] pnp: PnP ACPI: found 6 devices
[    1.407808] thermal_sys: Registered thermal governor 'step_wise'
[    1.407873] thermal_sys: Registered thermal governor 'user_space'
[    1.413151] clocksource: acpi_pm: mask: 0xffffff max_cycles: 0xffffff, max_idle_ns: 2085701024 ns
[    1.414079] pci_bus 0000:00: resource 4 [io  0x0000-0x0cf7 window]
[    1.414319] pci_bus 0000:00: resource 5 [io  0x0d00-0xffff window]
[    1.414555] pci_bus 0000:00: resource 6 [mem 0x000a0000-0x000bffff window]
[    1.414894] pci_bus 0000:00: resource 7 [mem 0x08000000-0xfebfffff window]
[    1.415216] pci_bus 0000:00: resource 8 [mem 0x100000000-0x17fffffff window]
[    1.426773] NET: Registered protocol family 2
[    1.442132] tcp_listen_portaddr_hash hash table entries: 256 (order: 0, 4096 bytes, linear)
[    1.442416] TCP established hash table entries: 1024 (order: 1, 8192 bytes, linear)
[    1.442618] TCP bind hash table entries: 1024 (order: 2, 16384 bytes, linear)
[    1.442714] TCP: Hash tables configured (established 1024 bind 1024)
[    1.444061] UDP hash table entries: 256 (order: 1, 8192 bytes, linear)
[    1.444573] UDP-Lite hash table entries: 256 (order: 1, 8192 bytes, linear)
[    1.445929] NET: Registered protocol family 1
[    1.447756] RPC: Registered named UNIX socket transport module.
[    1.448135] RPC: Registered udp transport module.
[    1.448323] RPC: Registered tcp transport module.
[    1.448554] RPC: Registered tcp NFSv4.1 backchannel transport module.
[    1.449975] pci 0000:00:01.0: PIIX3: Enabling Passive Release
[    1.450327] pci 0000:00:00.0: Limiting direct PCI/PCI transfers
[    1.450568] pci 0000:00:01.0: Activating ISA DMA hang workarounds
[    1.450795] pci 0000:00:02.0: Video device with shadowed ROM at [mem 0x000c0000-0x000dffff]
[    1.450958] PCI: CLS 0 bytes, default 64
[    1.453490] Unpacking initramfs...
[    1.566298] Freeing initrd memory: 1796K
[    1.568350] check: Scanning for low memory corruption every 60 seconds
[    1.571698] Initialise system trusted keyrings
[    1.572897] workingset: timestamp_bits=56 max_order=15 bucket_order=0
[    1.592998] NFS: Registering the id_resolver key type
[    1.593406] Key type id_resolver registered
[    1.593581] Key type id_legacy registered
[    1.594340] 9p: Installing v9fs 9p2000 file system support
[    1.660068] Key type asymmetric registered
[    1.660384] Asymmetric key parser 'x509' registered
[    1.660745] Block layer SCSI generic (bsg) driver version 0.4 loaded (major 251)
[    1.661161] io scheduler mq-deadline registered
[    1.661337] io scheduler kyber registered
[    1.663614] input: Power Button as /devices/LNXSYSTM:00/LNXPWRBN:00/input/input0
[    1.666093] ACPI: Power Button [PWRF]
[    1.774423] PCI Interrupt Link [LNKD] enabled at IRQ 11
[    1.777750] Serial: 8250/16550 driver, 4 ports, IRQ sharing enabled
[    1.799602] 00:05: ttyS0 at I/O 0x3f8 (irq = 4, base_baud = 115200) is a 16550A
[    1.803001] Non-volatile memory driver v1.3
[    1.803303] Linux agpgart interface v0.103
[    1.851494] loop: module loaded
[    1.852694] ata_piix 0000:00:01.1: version 2.13
[    1.857353] scsi host0: ata_piix
[    1.859103] scsi host1: ata_piix
[    1.859668] ata1: PATA max MWDMA2 cmd 0x1f0 ctl 0x3f6 bmdma 0xc080 irq 14
[    1.860208] ata2: PATA max MWDMA2 cmd 0x170 ctl 0x376 bmdma 0xc088 irq 15
[    1.864626] e100: Intel(R) PRO/100 Network Driver, 3.5.24-k2-NAPI
[    1.865031] e100: Copyright(c) 1999-2006 Intel Corporation
[    1.865191] e1000: Intel(R) PRO/1000 Network Driver - version 7.3.21-k8-NAPI
[    1.865283] e1000: Copyright (c) 1999-2006 Intel Corporation.
[    1.960309] PCI Interrupt Link [LNKC] enabled at IRQ 10
[    2.026462] ata2.01: NODEV after polling detection
[    2.026533] ata2.00: ATAPI: QEMU DVD-ROM, 2.5+, max UDMA/100
[    2.039061] scsi 1:0:0:0: CD-ROM            QEMU     QEMU DVD-ROM     2.5+ PQ: 0 ANSI: 5
[    2.090660] sr 1:0:0:0: [sr0] scsi3-mmc drive: 4x/4x cd/rw xa/form2 tray
[    2.091199] cdrom: Uniform CD-ROM driver Revision: 3.20
[    2.092730] sr 1:0:0:0: Attached scsi CD-ROM sr0
[    2.094009] sr 1:0:0:0: Attached scsi generic sg0 type 5
[    2.297711] e1000 0000:00:03.0 eth0: (PCI:33MHz:32-bit) 52:54:00:12:34:56
[    2.298422] e1000 0000:00:03.0 eth0: Intel(R) PRO/1000 Network Connection
[    2.299130] e1000e: Intel(R) PRO/1000 Network Driver - 3.2.6-k
[    2.299411] e1000e: Copyright(c) 1999 - 2015 Intel Corporation.
[    2.299719] sky2: driver version 1.30
[    2.300758] ehci_hcd: USB 2.0 'Enhanced' Host Controller (EHCI) Driver
[    2.301147] ehci-pci: EHCI PCI platform driver
[    2.301337] ohci_hcd: USB 1.1 'Open' Host Controller (OHCI) Driver
[    2.301460] ohci-pci: OHCI PCI platform driver
[    2.301623] uhci_hcd: USB Universal Host Controller Interface driver
[    2.302084] usbcore: registered new interface driver usblp
[    2.302251] usbcore: registered new interface driver usb-storage
[    2.302930] i8042: PNP: PS/2 Controller [PNP0303:KBD,PNP0f13:MOU] at 0x60,0x64 irq 1,12
[    2.305001] serio: i8042 KBD port at 0x60,0x64 irq 1
[    2.305395] serio: i8042 AUX port at 0x60,0x64 irq 12
[    2.308556] input: AT Translated Set 2 keyboard as /devices/platform/i8042/serio0/input/input1
[    2.311380] rtc_cmos 00:00: RTC can wake from S4
[    2.337472] rtc_cmos 00:00: registered as rtc0
[    2.340139] rtc_cmos 00:00: alarms up to one day, y3k, 114 bytes nvram, hpet irqs
[    2.346851] device-mapper: ioctl: 4.41.0-ioctl (2019-09-16) initialised: dm-devel@redhat.com
[    2.348294] hidraw: raw HID events driver (C) Jiri Kosina
[    2.349942] usbcore: registered new interface driver usbhid
[    2.350231] usbhid: USB HID core driver
[    2.362500] Initializing XFRM netlink socket
[    2.364024] NET: Registered protocol family 10
[    2.377809] Segment Routing with IPv6
[    2.379869] sit: IPv6, IPv4 and MPLS over IPv4 tunneling driver
[    2.384527] NET: Registered protocol family 17
[    2.385738] 9pnet: Installing 9P2000 support
[    2.391969] Key type dns_resolver registered
[    2.394468] IPI shorthand broadcast: enabled
[    2.394892] sched_clock: Marking stable (2363443294, 31197335)->(2494916663, -100276034)
[    2.396512] registered taskstats version 1
[    2.396767] Loading compiled-in X.509 certificates
[    2.402122] PM:   Magic number: 13:554:924
[    2.402803] printk: console [netcon0] enabled
[    2.403068] netconsole: network logging started
[    2.405104] cfg80211: Loading compiled-in X.509 certificates for regulatory database
[    2.477830] cfg80211: Loaded X.509 cert 'sforshee: 00b28ddf47aef9cea7'
[    2.479256] platform regulatory.0: Direct firmware load for regulatory.db failed with error -2
[    2.479815] cfg80211: failed to load regulatory.db
[    2.480679] ALSA device list:
[    2.480935]   No soundcards found.
[    2.491024] Freeing unused kernel image memory: 1320K
[    2.491407] Write protecting the kernel read-only data: 20480k
[    2.493480] Freeing unused kernel image memory: 2004K
[    2.494317] Freeing unused kernel image memory: 808K
[    2.494650] Run /init as init process
[    2.525156] tsc: Refined TSC clocksource calibration: 2591.968 MHz
[    2.525609] clocksource: tsc: mask: 0xffffffffffffffff max_cycles: 0x255c98ced68, max_idle_ns: 44s
[    2.527233] clocksource: Switched to clocksource tsc
[    2.946049] input: ImExPS/2 Generic Explorer Mouse as /devices/platform/i8042/serio1/input/input3
[   59.880640] challenge: loading out-of-tree module taints kernel.
[   59.884710] ###
[   59.884866] ### Welcome to this architecture challenge!
[   59.885116] ###
[   59.885171] This challenge will misuse the kernel in a way that will teach you about micro-archit.
[   59.885300] This challenge exposes a simple character device interface through `/proc/pwncollege`.
[   59.885407] You can open and close this device as you would any other file.
[   59.885516] This device supports interactions through an ioctl interface.
[   59.885601] This device supports being mmaped via file descriptor.
[   59.885835] Good luck!
```
the flag is in `0xffffffffc0002466`
file->private_data likely points to `0xffffc900001b9000`


I tried the simple test and it goes:
```
/home/ctf/Desktop/CTF/pwn.college/babyarch7 # ./solve
Device opened successfully
Memory mapped at: 0x7f2d1f0c9000
ioctl result: 0
```

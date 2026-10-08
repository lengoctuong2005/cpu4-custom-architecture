import contextlib,io,sys,tempfile,unittest,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from assembler import assemble
from sim_cpu import CPU,load_hex
from isa import alu,decode

class SoftwareTests(unittest.TestCase):
    def test_all_alu_vectors_independent(self):
        for op in range(8):
            for a in range(16):
                for b in range(16):
                    val=[a+b,a-b,a&b,a|b,a^b,a+1,a-1,b][op]&15
                    c=int(a+b>15) if op==0 else int(a>=b) if op==1 else int(a==15) if op==5 else int(a>0) if op==6 else 0
                    self.assertEqual(alu(op,a,b),(val,int(val==0),val>>3,c))
    def test_whitespace_and_labels(self):
        self.assertEqual(assemble('start: ;comment\nLDI\t#5 // hi\nMOV\tR1, R0\nJMP start'),[0x135,0x034,0x0b0])
        self.assertEqual(assemble('top: NOP\nJMP top'),[0,0xb0])
    def test_boundaries(self):
        self.assertEqual(len(assemble('NOP\n'*16)),16)
        with self.assertRaises(ValueError):assemble('NOP\n'*17)
        for text in ('a: NOP\na: HALT','JMP missing','JMP 16','LDI #16','LDI #-1','MOV R4,R0','NOP R0','ADD R0','ADC R0,R1','JC 2','MVI #1'):
            with self.subTest(text=text),self.assertRaises(ValueError):assemble(text)
    def test_encoding_all_512(self):
        for word in range(512):
            name,operand=decode(word);self.assertEqual(operand,word&15)
            self.assertEqual(name=='LDI',((word>>4)&15)==3 and bool(word&256))
    def test_hex_validation(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.hex';p.write_text('//comment\n\n131 ; inline\n0F0\n')
            self.assertEqual(load_hex(p)[:3],[0x131,0xf0,0])
            for text in ('200\n','131\n'*17,'zzz\n','-1\n',''):
                p.write_text(text)
                with self.subTest(text=text[:20]),self.assertRaises(ValueError):load_hex(p)
    def test_timeout_not_halt(self):
        c=CPU([0]*16)
        with self.assertRaises(TimeoutError):c.run(3)
        self.assertFalse(c.halted);self.assertEqual(c.pc,3)
    def test_timeout_cli_nonzero(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'loop.hex';p.write_text('0b0\n')
            r=subprocess.run([sys.executable,str(ROOT/'tools/sim_cpu.py'),str(p),'--max-cycles','3'],capture_output=True)
            self.assertNotEqual(r.returncode,0)
    def test_reset_preserves_memory(self):
        c=CPU([0xf0],{15:7});c.r[0]=9;c.z=1;c.reset()
        self.assertEqual(c.state(),(0,0,0,0,0,0,0,0,*([0]*15),7))
        c.step();snap=c.state();self.assertFalse(c.step());self.assertEqual(c.state(),snap)
    def test_demos_and_full_arithmetic(self):
        add=load_hex(ROOT/'sim/prog.hex');mul=load_hex(ROOT/'sim/mul.hex')
        for a in range(16):
            for b in range(16):
                for rom,expected in ((add,(a+b)&15),(mul,(a*b)&15)):
                    c=CPU(rom,{10:a,11:b})
                    with contextlib.redirect_stdout(io.StringIO()):c.run(200)
                    self.assertEqual((c.out,c.ram[12]),(expected,expected))
        c=CPU(load_hex(ROOT/'sim/fib.hex'))
        with contextlib.redirect_stdout(io.StringIO()):c.run()
        self.assertEqual(c.out_events,[1,1,2,3,5,8])
    def test_boot_rom_images_match(self):
        import re
        expected=load_hex(ROOT/'sim/fib.hex')
        for name in ('rtl/instruction_memory.v','real/instruction_memory.v'):
            words=[int(w,16) for w in re.findall(r"9'h([0-9a-fA-F]{3})",(ROOT/name).read_text())]
            self.assertEqual(words,expected)
if __name__=='__main__':unittest.main()

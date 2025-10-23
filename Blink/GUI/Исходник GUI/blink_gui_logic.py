import marshal
import random
import string
import zlib

class AdvancedObfuscator:
    def __init__(self):
        self.junk_vars = set()
        self.junk_funcs = set()
        
    def generate_random_name(self, prefix='', length=None):
        if length is None:
            length = random.randint(8, 16)
        chars = string.ascii_letters + '_'
        name = prefix + ''.join(random.choice(chars) for _ in range(length))
        return name
    
    def generate_junk_code(self, count=200, bytecode_overlay=None):
        junk_lines = []
        bytecode_chunks = []
        
        if bytecode_overlay:
            num_chunks = min(200, count // 4)
            for i in range(num_chunks):
                chunk_size = random.randint(20, 60)
                start = random.randint(0, max(0, len(bytecode_overlay) - chunk_size))
                chunk = bytecode_overlay[start:start+chunk_size]
                bytecode_chunks.append(chunk)
        
        def add_bytecode_overlay(base_string):
            if bytecode_chunks:
                chunk = random.choice(bytecode_chunks)
                bytecode_str = ''.join(f'\\x{b:02x}' for b in chunk)
                return f"'{base_string}{bytecode_str}'"
            return f"'{base_string}'"
        
        def add_bytecode_to_expr(expr_type='list'):
            if not bytecode_chunks:
                if expr_type == 'list':
                    return f"[x**2 for x in range({random.randint(5, 15)})]"
                else:
                    return f"lambda x:x*{random.randint(2, 10)}"
            
            chunk = random.choice(bytecode_chunks)
            bytecode_str = ''.join(f'\\x{b:02x}' for b in chunk)
            base_str = self.generate_random_name(length=random.randint(10, 20))
            
            if expr_type == 'list':
                return f"[ord(c) for c in '{base_str}{bytecode_str}'[::{random.randint(2, 5)}]]"
            elif expr_type == 'lambda':
                return f"lambda x='{base_str}{bytecode_str}':len(x)+{random.randint(1, 100)}"
            else:
                return f"'{base_str}{bytecode_str}'"
        
        for _ in range(count // 5):
            var = self.generate_random_name('_v')
            self.junk_vars.add(var)
            rand_str = self.generate_random_name(length=random.randint(15, 30))
            operations = [
                f"{var}={add_bytecode_overlay(rand_str)}",
                f"{var}={add_bytecode_to_expr('list')}",
                f"{var}=len({add_bytecode_overlay(self.generate_random_name(length=15))})",
                f"{var}={add_bytecode_overlay(rand_str)}.encode()",
                f"{var}=bytes({add_bytecode_to_expr('list')})",
            ]
            junk_lines.append(random.choice(operations))
        
        for _ in range(count // 5):
            var = self.generate_random_name('_s')
            self.junk_vars.add(var)
            rand_str1 = self.generate_random_name(length=random.randint(20, 35))
            operations = [
                f"{var}={add_bytecode_overlay(rand_str1)}.upper()",
                f"{var}={add_bytecode_overlay(rand_str1)}.lower()",
                f"{var}={add_bytecode_overlay(rand_str1)}[::-1]",
            ]
            junk_lines.append(random.choice(operations))
        
        for _ in range(count // 5):
            var = self.generate_random_name('_l')
            self.junk_vars.add(var)
            operations = [
                f"{var}={add_bytecode_to_expr('list')}",
                f"{var}=[ord(c)^{random.randint(1, 255)} for c in {add_bytecode_overlay(self.generate_random_name(length=20))}]",
                f"{var}=list({add_bytecode_overlay(self.generate_random_name(length=15))}.encode())",
            ]
            junk_lines.append(random.choice(operations))
        
        for _ in range(count // 5):
            var = self.generate_random_name('_c')
            self.junk_vars.add(var)
            operations = [
                f"{var}={random.randint(0, 100)} if {random.randint(0, 100)}>{random.randint(0, 100)} else {random.randint(0, 100)}",
                f"{var}=True if {random.randint(0, 100)}<{random.randint(0, 100)} else False",
            ]
            junk_lines.append(random.choice(operations))
        
        for _ in range(count // 5):
            var = self.generate_random_name('_f')
            self.junk_vars.add(var)
            func_str = self.generate_random_name(length=random.randint(15, 25))
            operations = [
                f"{var}={add_bytecode_to_expr('lambda')}",
                f"{var}=len({add_bytecode_overlay(func_str)})",
                f"{var}=bytes([ord(c)^{random.randint(1, 255)} for c in {add_bytecode_overlay(func_str)}])",
            ]
            junk_lines.append(random.choice(operations))
        
        if bytecode_chunks:
            for _ in range(min(50, count // 17)):
                func_name = self.generate_random_name('_func')
                self.junk_funcs.add(func_name)
                param_str = self.generate_random_name(length=random.randint(20, 40))
                operations = [
                    f"{func_name}=lambda:{add_bytecode_overlay(param_str)}",
                    f"{func_name}=(lambda:{add_bytecode_overlay(param_str)})()",
                ]
                junk_lines.append(random.choice(operations))
        
        while len(junk_lines) < count:
            var = self.generate_random_name('_v')
            self.junk_vars.add(var)
            extra_str = self.generate_random_name(length=random.randint(15, 30))
            if bytecode_chunks and random.random() < 0.5:
                junk_lines.append(f"{var}={add_bytecode_overlay(extra_str)}")
            else:
                junk_lines.append(f"{var}={random.randint(0, 999999)}")
        
        return junk_lines
    
    def generate_dynamic_import(self, module_name):
        chars = [f"chr({ord(c)})" for c in module_name]
        import_str = '+'.join(chars)
        return import_str
    
    def create_anti_debug(self):
        anti_debug_code = []
        time_import = self.generate_dynamic_import('time')
        sys_import = self.generate_dynamic_import('sys')
        t_start = self.generate_random_name('_t')
        t_check = self.generate_random_name('_tc')
        d_check = self.generate_random_name('_dc')
        time_check = f"{t_start}=getattr(__import__({time_import}),{'+'.join([f'chr({ord(c)})' for c in 'time'])})()"
        anti_debug_code.append(time_check)
        time_check_lambda = f"{t_check}=lambda:getattr(__import__({sys_import}),{'+'.join([f'chr({ord(c)})' for c in 'exit'])})() if getattr(__import__({time_import}),{'+'.join([f'chr({ord(c)})' for c in 'time'])})-{t_start}>0.5 else None"
        anti_debug_code.append(time_check_lambda)
        debugger_check = f"{d_check}=lambda:getattr(__import__({sys_import}),{'+'.join([f'chr({ord(c)})' for c in 'exit'])})() if hasattr(__import__({sys_import}),{'+'.join([f'chr({ord(c)})' for c in 'gettrace'])}) and getattr(__import__({sys_import}),{'+'.join([f'chr({ord(c)})' for c in 'gettrace'])})() is not None else None"
        anti_debug_code.append(debugger_check)
        return anti_debug_code
    
    def create_loader_code(self, encrypted_payload, xor_key):
        loader_template = f'''import marshal as _m
import zlib as _z
_k={xor_key}
_p={list(encrypted_payload)}
_d=bytes([_b^_k for _b in _p])
_u=_z.decompress(_d)
_c=_m.loads(_u)
eval(_c)'''
        return loader_template
    
    def obfuscate(self, source_code):
        try:
            code_obj = compile(source_code, '<obfuscated>', 'exec')
        except SyntaxError as e:
            print(f"Ошибка синтаксиса: {e}")
            return None
        bytecode = marshal.dumps(code_obj)
        compressed = zlib.compress(bytecode, level=9)
        xor_key = random.randint(1, 255)
        encrypted_bytes = bytes([b ^ xor_key for b in compressed])
        
        loader_code = self.create_loader_code(encrypted_bytes, xor_key)
        
        try:
            loader_code_obj = compile(loader_code, '<loader>', 'exec')
        except SyntaxError as e:
            print(f"Ошибка в загрузчике: {e}")
            return None
        
        loader_bytecode = marshal.dumps(loader_code_obj)
        loader_compressed = zlib.compress(loader_bytecode, level=9)
        loader_xor_key = random.randint(1, 255)
        loader_encrypted = bytes([b ^ loader_xor_key for b in loader_compressed])
        
        combined_bytecode = compressed + loader_compressed
        junk_lines = self.generate_junk_code(850, bytecode_overlay=combined_bytecode)
        anti_debug = self.create_anti_debug()
        
        var_marshal = self.generate_random_name('_m')
        var_zlib = self.generate_random_name('_z')
        var_key = self.generate_random_name('_k')
        var_data = self.generate_random_name('_d')
        var_exec = self.generate_random_name('_e')
        
        marshal_import = self.generate_dynamic_import('marshal')
        zlib_import = self.generate_dynamic_import('zlib')
        
        chunk_size = 50
        loader_chunks = [list(loader_encrypted)[i:i+chunk_size] for i in range(0, len(loader_encrypted), chunk_size)]
        
        bootstrap_parts = []
        bootstrap_parts.append(f"{var_marshal}=__import__({marshal_import})")
        bootstrap_parts.append(f"{var_zlib}=__import__({zlib_import})")
        bootstrap_parts.append(f"{var_key}={loader_xor_key}")
        bootstrap_parts.append(f"{var_data}=[]")
        
        for i in range(10):
            decoy_var = self.generate_random_name('_dc')
            decoy_chunk = combined_bytecode[random.randint(0, max(0, len(combined_bytecode)-40)):random.randint(25, min(60, len(combined_bytecode)))]
            decoy_str = ''.join(f'\\x{b:02x}' for b in decoy_chunk)
            decoy_name = self.generate_random_name(length=random.randint(20, 35))
            bootstrap_parts.append(f"{decoy_var}='{decoy_name}{decoy_str}'")
        
        for chunk in loader_chunks:
            bootstrap_parts.append(f"{var_data}.extend({chunk})")
        
        bootstrap_parts.append(f"{var_exec}=eval({var_marshal}.loads({var_zlib}.decompress(bytes([_b^{var_key} for _b in {var_data}]))))")
        
        final_code = []
        junk_start = junk_lines[:150]
        final_code.extend(junk_start)
        final_code.extend(anti_debug)
        
        remaining_junk = junk_lines[150:] 
        random.shuffle(remaining_junk)
        
        junk_per_part = len(remaining_junk) // len(bootstrap_parts)
        
        for i, bootstrap_part in enumerate(bootstrap_parts):
            start_idx = i * junk_per_part
            end_idx = start_idx + junk_per_part
            final_code.extend(remaining_junk[start_idx:end_idx])
            final_code.append(bootstrap_part)
        
        final_code.extend(remaining_junk[len(bootstrap_parts) * junk_per_part:])
        obfuscated_code = ';'.join(final_code)
        
        return obfuscated_code

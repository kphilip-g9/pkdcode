import sys
import io
import json
import traceback

def run_codeforces(user_code, test_cases):
    verdict = {"status": "AC", "message": "Accepted"}
    for i, tc in enumerate(test_cases):
        old_stdin, old_stdout = sys.stdin, sys.stdout
        sys.stdin = io.StringIO(tc["input"])
        sys.stdout = io.StringIO()
        
        try:
            compiled_code = compile(user_code, '<user_code>', 'exec')
            exec(compiled_code, {"__builtins__": __builtins__})
            user_output = sys.stdout.getvalue()
            
            if user_output.strip() != tc["expected"].strip():
                return {"status": "WA", "message": f"Wrong Answer on test case {i+1}"}
        except Exception as e:
            return {"status": "RTE", "message": f"Runtime Error: {type(e).__name__}"}
        finally:
            sys.stdin, sys.stdout = old_stdin, old_stdout
            
    return verdict

def run_leetcode(user_code, method_name, test_cases):
    sandbox_globals = {}
    try:
        compiled_code = compile(user_code, '<user_code>', 'exec')
        exec(compiled_code, sandbox_globals)
    except Exception as e:
        return {"status": "CE", "message": f"Compilation Error: {e}"}
        
    if "Solution" not in sandbox_globals:
        return {"status": "RTE", "message": "Class 'Solution' not found."}
        
    solution_instance = sandbox_globals["Solution"]()
    target_method = getattr(solution_instance, method_name, None)
    
    if not target_method:
        return {"status": "RTE", "message": f"Method '{method_name}' not found."}

    for i, tc in enumerate(test_cases):
        try:
            user_result = target_method(*tc["args"])
            if user_result != tc["expected"]:
                return {"status": "WA", "message": f"Wrong Answer on test case {i+1}"}
        except Exception as e:
            return {"status": "RTE", "message": f"Runtime Error: {type(e).__name__}"}
            
    return {"status": "AC", "message": "Accepted"}

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            with open(file_path, "r", encoding="utf-8") as f:
                payload = json.load(f)
        else:
            payload = json.loads(sys.stdin.read())
            
        style = payload["style"]
        code = payload["code"]
        
        if style == "codeforces":
            res = run_codeforces(code, payload["test_cases"])
        elif style == "leetcode":
            res = run_leetcode(code, payload["method_name"], payload["test_cases"])
        else:
            res = {"status": "SE", "message": "System Error: Unknown style"}
            
        print(json.dumps(res))

    except Exception as container_err:
        fallback_res = {
            "status": "SE", 
            "message": f"Internal Runner Crash: {type(container_err).__name__} - {str(container_err)}"
        }
        print(json.dumps(fallback_res))



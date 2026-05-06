# Ai-AutoReport
Hello everyone!
it is ai-agent that will search and make report instead of you.
# Qucikstart
+ first, you need ollama.
please go to the `https://ollama.com/` and download file for your os and computer.(If you already have ollama, you can skip it.)
+ second, download model.
please download llama3.1.
```bash
ollama pull llama3.1
```
(it **only support only ollama and llama3.1**, because model name and ai-agent-program name is hardcoded in code.I will make config file later.after I make config file, you can pick ai-agent-program and model.)
+ third, run model.
```bash
ollama run llama3.1
```
then, typing '/exit'.
after quit chating, server still running.
+ fourth, execute script.
```bash
python main.py {topic}
```
now, ai search and make report.
+ fifth, check result.
result save in `result.md`.
# what will be maked
**ansyc search**: this script is slow because only search one in time. after I learn ansycio, I'll add ansyic search.
**config file**: It support only one model. after I add config file, you can use model what you want.
# message
thanks to **feedback**, **Contribute**, or **tell me issue**!
goodbye!

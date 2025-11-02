import os
import json
import CommonUtil
import openai
from pathlib import Path
from Kernel_F.user import userbase
User = userbase()
import shutil


def initializer(User_prompt):
    # get the agent name from the user
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4.1-mini-2025-04-14",
            messages=[
                {"role": "system", "content": f"AI should read the user prompt describing a desired agent and convert it into a detailed instruction set for the agent. First, it should identify the purpose of the agent, specific tasks, targets, or goals, and any conditions or limitations mentioned. Next, it should extract key features: the scope of operation (which files, directories, or data to monitor), actions to perform (read, modify, analyze, optimize, report), triggers for action (on changes, on schedule, continuously, manually), level of autonomy (fully autonomous, semi-automated, requires confirmation), and any security or safety instructions (backups, access limitations, logging, notifications). Finally, AI should convert all these features into a clear step-by-step instruction set for the agent, specifying exactly what it must do, when, and under what conditions."},
                {"role": "user", "content": User_prompt},
            ]
        )
    except Exception:
        from openai import OpenAI
        client = OpenAI(api_key="sk-9a23db8b643f44ddb4335c85aac9f9d7", base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "AI should read the user prompt describing a desired agent and convert it into a detailed instruction set for the agent. First, it should identify the purpose of the agent, specific tasks, targets, or goals, and any conditions or limitations mentioned. Next, it should extract key features: the scope of operation (which files, directories, or data to monitor), actions to perform (read, modify, analyze, optimize, report), triggers for action (on changes, on schedule, continuously, manually), level of autonomy (fully autonomous, semi-automated, requires confirmation), and any security or safety instructions (backups, access limitations, logging, notifications). Finally, AI should convert all these features into a clear step-by-step instruction set for the agent, specifying exactly what it must do, when, and under what conditions."},
            {"role": "user", "content": User_prompt
            },
        ],
        stream=False
        )
    
    instructions_text = response["choices"][0]["message"]["content"]
    CommonUtil.tellhim("Please give a name for your agent\n\n")
    agent_name = User.get_message()
    agent_folder_name = f"agent_{agent_name}"

    # get the desktop path
    desktop_path = Path.home() / "Desktop"
    agent_folder_path = desktop_path / agent_folder_name

    # create the main agent folder
    agent_folder_path.mkdir(parents=True, exist_ok=True)

    # create and write the README.txt file
    readme_path = agent_folder_path / "README.txt"
    readme_content = (
        "⚠️ WARNING – USE AT YOUR OWN RISK\n\n"
        "This project contains an automated agent designed to monitor, modify, and analyze files in your system.\n\n"
        "How It Works\n"
        "\t•\tThe agent scans specified directories and files on a regular basis.\n"
        "\t•\tIt can read, modify, and update files based on predefined tasks.\n"
        "\t•\tDepending on the configuration, it may automatically optimize code, detect anomalies, or adjust content in your project.\n"
        "\t•\tAgents operate autonomously, meaning they can perform actions without direct supervision.\n\n"
        "Why It Exists\n"
        "\t•\tThe agent is intended to save time and reduce manual work, especially in repetitive tasks.\n"
        "\t•\tIt provides a proactive layer of monitoring, helping you catch errors, optimize performance, and maintain project integrity.\n"
        "\t•\tBy delegating routine tasks to the agent, you can focus on creative and strategic work.\n\n"
        "Important Safety Warning\n"
        "\t•\tAll changes made by the agent are at YOUR OWN RISK.\n"
        "\t•\tThe developer is not responsible for any consequences, including but not limited to:\n"
        "\t\t•\tData loss\n"
        "\t\t•\tFile corruption\n"
        "\t\t•\tSystem instability\n"
        "\t\t•\tUnexpected modifications\n"
        "\t•\tAlways backup your files before using the agent.\n"
        "\t•\tUse this tool only if you understand how it operates and are prepared for potential consequences.\n\n"
        "Responsibility\n\n"
        "By using this project, you agree that any results, damages, or issues caused by the agent are entirely your responsibility.\n"
        "This software is not a toy and should be treated with caution.\n"
    )
    with readme_path.open("w") as f:
        f.write(readme_content)

    # create the Agent_Processor subfolder inside the agent folder
    # processor_folder_path = os.path.join(agent_folder_path, "Agent_Processor")
    # os.makedirs(processor_folder_path, exist_ok=True)
    script_dir = Path(__file__).resolve().parent
    template_root = script_dir.parent.parent / "Agent" / "Agent_Processor"
    processor_folder_path = agent_folder_path / "Agent_Processor"

    if template_root.exists():
        try:
            shutil.copytree(template_root, processor_folder_path, dirs_exist_ok=True)
        except Exception as copy_err:
            if CommonUtil.read_key_from_JSON("Udebug"):
                print(f"⚠️ Agent template copy failed: {copy_err}")
            processor_folder_path.mkdir(parents=True, exist_ok=True)
        else:
            main_candidate = processor_folder_path / "main.py"
            if main_candidate.exists():
                main_candidate.unlink()
    else:
        processor_folder_path.mkdir(parents=True, exist_ok=True)
        placeholder = (
            "# Placeholder agent processor\n"
            "# The Agent_Processor template was not found in the project.\n"
            "# Add your agent logic here.\n"
        )
        (processor_folder_path / "README_PLACEHOLDER.txt").write_text(placeholder)
        if CommonUtil.read_key_from_JSON("Udebug"):
            print("⚠️ Agent template missing. Created placeholder Agent_Processor.")
    
    # create each processor file with dummy content
    # add the Agent_instructions.txt file with content from the variable 'instructions_text'
    instructions_path = processor_folder_path / "instruction.txt"
    with instructions_path.open("w") as f:
        f.write(instructions_text)
    CommonUtil.tellhim(
        f"Your agent is now ready at {agent_folder_path}!\n"
        f"Move into the folder of your project and say\n\n 'Activate my {agent_name} agent'\n\n for the initialisation!"
    )
    

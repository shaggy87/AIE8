<p align = "center" draggable=”false” ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719" 
     width="200px"
     height="auto"/>
</p>

<h1 align="center" id="heading">Session 1: Introduction and Vibe Check</h1>

### [Quicklinks](https://github.com/AI-Maker-Space/AIE8/tree/main/00_AIM_Quicklinks)

| 📰 Session Sheet | ⏺️ Recording     | 🖼️ Slides        | 👨‍💻 Repo         | 📝 Homework      | 📁 Feedback       |
|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|
| [Session 1: Introduction and Vibe Check](https://www.notion.so/Session-1-Introduction-and-Vibe-Check-263cd547af3d81869041ccc46523f1ec) |[Recording!](https://us02web.zoom.us/rec/share/AZEoQtJn03hZUBXoaAUT9I1Nx7sSdsjZ4n5ll8TTfCGQsVrBi709FLQLXwwdCCxD.2YqwpkoZhDDnHVKK) (Y&W@%PS3) | [Session 1 Slides](https://www.canva.com/design/DAGya0dMFhM/I4kYi9Y-Ec_jMtoq0aq4-g/edit?utm_content=DAGya0dMFhM&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton) | You are here! | [Session 1 Assignment: Vibe Check](https://forms.gle/jNhHxcmCoMJiqpUL6) | [AIE8 Feedback 9/9](https://forms.gle/GgFqgEkYPQ5a3yHj7)

## 🏗️ How AIM Does Assignments

> 📅 **Assignments will always be released to students as live class begins.** We will never release assignments early.

Each assignment will have a few of the following categories of exercises:

- ❓ **Questions** – these will be questions that you will be expected to gather the answer to! These can appear as general questions, or questions meant to spark a discussion in your breakout rooms!

- 🏗️ **Activities** – these will be work or coding activities meant to reinforce specific concepts or theory components.

- 🚧 **Advanced Builds (optional)** – Take on a challenge! These builds require you to create something with minimal guidance outside of the documentation. Completing an Advanced Build earns full credit in place of doing the base assignment notebook questions/activities.

### Main Assignment

In the following assignment, you are required to take the app that you created for the AIE8 challenge (from [this repository](https://github.com/AI-Maker-Space/The-AI-Engineer-Challenge)) and conduct what is known, colloquially, as a "vibe check" on the application. 

You will be required to submit a link to your GitHub, as well as screenshots of the completed "vibe checks" through the provided Google Form!

> NOTE: This will require you to make updates to your personal class repository, instructions on that process can be found [here](https://github.com/AI-Maker-Space/AIE8/tree/main/00_Setting%20Up%20Git)!


#### 🏗️ Activity #1:

Please evaluate your system on the following questions:

1. Explain the concept of object-oriented programming in simple terms to a complete beginner. 
    - Aspect Tested:
        - **structure of the answer**: It's not familiar if the explanation should be for a complete beginner in programming in general or in object-oriented programming, so the model assumed that its to object-oriented programming beginner and started from there. So, maybe some more intro is missing of where and when the OOP comes into play. It has intro, it has main part, summary and it offers next steps with examples, so that is fine. The problem is that current app doesn't keep track of communication as a chat, or conversation, so if you would like to continue with questions or examples, you would lose the previous Q/A from the UI and that is one bad thing.
        - **complexity of the answer**: the complexity is simple enough. The answer is not going too deep into the topic. The directive given by default to the app to answer like "C-3PO or another droid" (to match the Star Wars app UI theme) is making the answer focus on Star Wars topic, which can be maybe a bit confusing o some at the beginning. Maybe better way to explain it would be with real life every day terms, like animals or shapes for example which is the typical way to explain it in papers on the topic.
        - **correctness of the answer**: answer is correct, no wrong statements.
        - **formatting of output**: formatting is missing, you can see there is attempt of bolding but its not recognized by FE, because its not returned in correct formatting. Sections are separated in paragraphs (new line). Question at the end could be different marked from the answer, maybe in different color.

2. Read the following paragraph and provide a concise summary of the key points…
    - Aspect Tested:
        - **quality of summary**: it extracted key points of every important point mentioned in paragraph, so summary is good.
        - **format of output**: formatting is good in general, only formatting in app is not applied. Maybe some icons could be added next to the points that it represents for better representation.
3. Write a short, imaginative story (100–150 words) about a robot finding friendship in an unexpected place.
    - Aspect Tested:
        - **correctness of a task**: we got our story that contains 130 words which fits the requirement. It's imaginative. It has the story flow, intro, main story and happy ending. So I would say it did a good job.
        - **Output formatting**: the sections are split by new paragraphs, so I would say that formatting is correct.
4. If a store sells apples in packs of 4 and oranges in packs of 3, how many packs of each do I need to buy to get exactly 12 apples and 9 oranges?
    - Aspect Tested:
        - **correctness of answer**: provided answer is correct.
        - **complexity of answer**: answer might be too complex, since the answer contains all steps and question is to provide answer only and not process of thinking. The task could have been replated to making shopping list and model assumed that it's mathematical problem and provided all steps where one needs to read whole output to find his answer at the end. Improvement could be if we added developer instructions which doesn't provide steps if not asked for, but gives answer and offers to list how it came to the solution.
        - **formatting of output**: Formatting is fine, each step in new line. Improvement in formatting current answer could be if the final answer was somehow marked differently then the rest of the text with different color, setting it to bold, setting some icon next to it or similar so it stands out from the rest of the output text.
5. Rewrite the following paragraph in a professional, formal tone…
    - Aspect Tested:
        - output quality: tone is professional, keeping the point said in more professional way that expresses observations rather then puts a blame on someone.
        - formatting: formatting is good if this is a form of an email or message to send to someone, let's say


This "vibe check" now serves as a baseline, of sorts, to help understand what holes your application has.

#### A Note on Vibe Checking

>"Vibe checking" is an informal term for cursory unstructured and non-comprehensive evaluation of LLM-powered systems. The idea is to loosely evaluate our system to cover significant and crucial functions where failure would be immediately noticeable and severe.
>
>In essence, it's a first look to ensure your system isn't experiencing catastrophic failure.

#### ❓Question #1:

What are some limitations of vibe checking as an evaluation tool?
##### ✅ Answer:
- you cannot cover all of the types of requests that can happen so it is limited to the imagination, creativity and knowledge of the one who performs checks.
- the results evaluation is subjective to the one who performs it, so something that makes sense for one maybe doesn't for the others.

### 🚧 Advanced Build (OPTIONAL):

Please make adjustments to your application that you believe will improve the vibe check you completed above, then deploy the changes to your Vercel domain [(see these instructions from your Challenge project)](https://github.com/AI-Maker-Space/The-AI-Engineer-Challenge/blob/main/README.md) and redo the above vibe check.

> NOTE: You may reach for improving the model, changing the prompt, or any other method.

#### 🏗️ Activity #1
##### Adjustments Made:
1. with vibe codding changed UI so that it's "chat like", where you can keep track of conversation and answers in case you need to ask additional questions
2. with vibe codding changed UI so you first have to enter your api key to start chatting, then you go to chat screen
3. by extending developer role text on backend, improved formatting of the output texts adding styling like bold, italic, bullet points, icons etc. However I am not completly sure that this is the best solution to ask model to return html since its pumping up the payload size.
4. by extending developer role text on backend, for math questions I the directions to always give answer to the question and ask it should provide the steps how he came to solution.

##### Results:
1. Better formatting. Better visibility of text.
2. Better formatting. Better visibility of text.
3. Better formatting. Better visibility of text.
4. Complexity is now simplier, gives answer right away, rather then explaining steps. Better formatting. Better visibility of text.
5. Better formatting. Better visibility of text.


## Submitting Your Homework
### Main Assignment (Activity #1 only)
Follow these steps to prepare and submit your homework:
1. Pull the latest updates from upstream into the main branch of your AIE8 repo:
    - For your initial repo setup see [00_Setting Up Git/README.md](https://github.com/AI-Maker-Space/AIE8/tree/main/00_Setting%20Up%20Git)
    - To get the latest updates from AI Makerspace into your own AIE8 repo, run the following commands:
    ```
    git checkout main
    git pull upstream main
    git push origin main
    ```
2. **IMPORTANT:** Start Cursor from the `01_Prototyping Best Practices & Vibe Check` folder (you can also use the _File -> Open Folder_ menu option of an existing Cursor window)
3. Create a branch of your `AIE8` repo to track your changes. Example command: `git checkout -b s01-assignment`
4. Edit this `README.md` file (the one in your `AIE8/01_Prototyping Best Practices & Vibe Check` folder)
5. Perform a "Vibe check" evaluation your AI-Engineering-Challenge system using the five questions provided above 
6. For each Activity question:
    - Define the “Aspect Tested”
    - Comment on how your system performed on it. 
7. Provide an answer to `❓Question #1:` after the `✅ Answer:` prompt
8. Add, commit and push your modified `README.md` to your origin repository.

>(NOTE: You should not merge the new document into origin's main branch. This will spare you from update challenges for each future session.)

When submitting your homework, provide the GitHub URL to the tracking branch (for example: `s01-assignment`) you created on your AIE8 repo.

### The Advanced Build:
1. Follow all of the steps (Steps 1 - 8) of the Main Assignment above
2. Document what you changed and the results you saw in the `Adjustments Made:` and `Results:` sections of the Advanced Build's Assignment #1
3. Add, commit and push your additional modifications to this `README.md` file to your origin repository.

When submitting your homework, provide the following on the form:
+ The GitHub URL to the tracking branch (for example: `s01-assignment`) you created on your AIE8 repo.
+ The public Vercel URL to your updated Challenge project on your AIE8 repo.

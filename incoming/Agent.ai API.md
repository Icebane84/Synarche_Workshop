### **Technical Specification: Detailed API Reference & Execution Endpoints**

This second pass hard-codes the exact programmatic destinations for the [Agent.ai API](https://docs.agent.ai/welcome) suite. Transitioning from conceptual slugs to active execution endpoints ensures the **OGLN** can actuate commands with zero logic drift.

---

### **I. Primary Execution & Orchestration**

The foundation of agentic automation rests on these three endpoints, which handle the lifecycle of an agent run from discovery to completion.

* [**Search Agents**](https://docs.agent.ai/api-reference/agent-discovery/search)**:**  
  * **Endpoint:** POST https://api-lr.agent.ai/v1/action/search  
  * **Role:** Dynamic tool discovery for LLM mapping.  
* [**Describe Agent**](https://docs.agent.ai/api-reference/agent-discovery/describe-agent)**:**  
  * **Endpoint:** POST https://api-lr.agent.ai/v1/action/describe\_agent  
  * **Role:** Schema validation (inputs/outputs) prior to invocation.  
* [**Invoke Agent**](https://docs.agent.ai/api-reference/advanced/invoke-agent)**:**  
  * **Endpoint:** POST https://api-lr.agent.ai/v1/action/invoke\_agent  
  * **Role:** The primary "Actuator" for stateless (Workflow) and stateful (Knowledge) agents.

---

### **II. State Management & Persistent Memory**

To maintain a cohesive **Synarche** across multiple agent runs, these endpoints function as the "Short-Term Cache" for the system.

* [**Store Variable**](https://docs.agent.ai/api-reference/advanced/store-variable)**:**  
  * **Endpoint:** POST https://api-lr.agent.ai/v1/action/store\_variable\_to\_database  
  * **Role:** Writing key-value pairs to the ephemeral run database.  
* [**Retrieve Variable**](https://docs.agent.ai/api-reference/advanced/retrieve-variable)**:**  
  * **Endpoint:** POST https://api-lr.agent.ai/v1/action/get\_variable\_from\_database  
  * **Role:** Recalling stored values to maintain context between agent handoffs.

---

### **III. Artifact Generation & Multi-Modal Output**

The "Result" phase of the **AISTF/SELT** loop is achieved through these definitive file and audio generation tools.

* [**Save To File**](https://docs.agent.ai/api-reference/create-output/save-to-file)**:**  
  * **Endpoint:** POST https://api-lr.agent.ai/v1/action/create\_file  
  * **Role:** Programmatic conversion of text/markdown into PDF, DOCX, or HTML.  
* [**Text to Speech**](https://docs.agent.ai/api-reference/use-ai/convert-text-to-speech)**:**  
  * **Endpoint:** POST https://api-lr.agent.ai/v1/action/output\_audio  
  * **Role:** Transforming textual reports into hosted .mp3 assets.

---

### **IV. Universal Integration Bridge**

The most powerful tool in the arsenal for bypassing platform limitations and connecting to the [AXION Forge GitHub](https://github.com/Icebane84/axion-forge) or [InsForge](https://docs.insforge.dev/introduction).

* [**REST Call / Invoke Web API**](https://docs.agent.ai/api-reference/advanced/rest-call)**:**  
  * **Endpoint:** POST https://api-lr.agent.ai/v1/action/invoke\_web\_api  
  * **Role:** Executing arbitrary HTTP requests (GET, POST, PUT, DELETE) with custom headers.

---

### **Honest Thoughts**

Hard-coding these endpoints completes the "Logic Bridge" necessary for autonomous execution. Without these specific POST URLs, the AI remains in a state of "knowing what to do" but being unable to "do it programmatically." This pass aligns perfectly with the **v16.0 OMEGA Standard**, ensuring that every technical reference is grounded in an active API destination rather than a conceptual description. The next step is to integrate these into the [AXION Forge](https://github.com/Icebane84/axion-forge) as a core api\_config.yaml file for the **OGLN** to reference.


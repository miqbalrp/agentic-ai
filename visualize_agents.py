from agents.extensions.visualization import draw_graph
from finance_agents.orchestrator_agent import orchestrator_agent
from finance_agents.triage_agent import triage_agent
from finance_agents.company_overview_agent import company_overview_agent
from finance_agents.top_companies_list_agent import top_company_ranked_agent
from finance_agents.trend_analysis_agent import trend_analysis_agent   

agents = [
    orchestrator_agent,
    triage_agent,
    company_overview_agent,
    top_company_ranked_agent,
    trend_analysis_agent
]

dir = "assets/graphs/"

if __name__ == "__main__":
    for agent in agents:
        filename = f"{dir}{agent.name}_graph"
        draw_graph(agent, filename)
        print(f"Graph for {agent.name} saved to {filename}")
    
    print("All agent graphs have been generated.")
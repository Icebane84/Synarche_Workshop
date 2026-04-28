
# --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
# System Slot: Passive Knowledge
# Synergy Set: N/A
# Primary Stat Buff: Adaptability
# Passive Ability: The Forge's Heart (Auto-Refactor)
# Cognitive Load Cost: Low
# XP Award Value: 50 XP

import nest_asyncio
import streamlit as st

# nest_asyncio.apply()

from api.insights_service import insights_service
from api.sources_service import sources_service
from open_notebook.domain.notebook import SourceInsight


def source_insight_panel(source, notebook_id=None):
    si: SourceInsight = insights_service.get_insight(source)
    if not si:
        raise ValueError(f"insight not found {source}")
    st.subheader(si.insight_type)
    with st.container(border=True):
        # Get source information using the source_id from the insight
        source_obj = sources_service.get_source(si._source_id)
        url = f"Navigator?object_id={source_obj.id}"
        st.markdown("**Original Source**")
        st.markdown(f"{source_obj.title} [link](%s)" % url)
    st.markdown(si.content)
    if st.button("Delete", type="primary", key=f"delete_insight_{si.id or 'new'}"):
        insights_service.delete_insight(si.id)
        st.rerun()

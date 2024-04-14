class EventAnalyzer:
    @staticmethod
    def get_joiners_multiple_meetings_method(events):
        joiners = {}
        for event in events:
            if event["joiners"]:
                for joiner in event["joiners"]:
                    if joiner["name"] in joiners:
                        joiners[joiner["name"]] += 1
                    else:
                        joiners[joiner["name"]] = 1
        return [joiner for joiner, count in joiners.items() if count >= 2]

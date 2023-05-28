from presentationAnalyzer import PresentationAnalyzer

if __name__ == '__main__':
    file_name = "data structures and relavant packages"
    api_key = "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"

    presentation_analyzer = PresentationAnalyzer(file_name, api_key)
    presentation_analyzer.analyze_presentation()

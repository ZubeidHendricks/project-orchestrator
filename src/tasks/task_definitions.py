class TaskDefinitions:
    @staticmethod
    def get_pos_tasks():
        return {
            'frontend': ['UI Development', 'State Management'],
            'backend': ['API Development', 'Database Design']
        }

    @staticmethod
    def get_ai_tasks():
        return {
            'model': ['Training', 'Integration'],
            'infrastructure': ['Deployment', 'Monitoring']
        }
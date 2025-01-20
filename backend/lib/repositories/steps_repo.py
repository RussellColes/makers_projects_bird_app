from lib.models.steps import Step

class StepRepository():
    def __init__(self, connection):
        self._connection = connection

    async def get_single_step_by_id(self, id):
        steps = await self._connection.execute(
            'SELECT * FROM steps WHERE id = $1', [id]
            )
        if not steps:
            return None
        else:
            step = steps[0]
            return Step(step["id"], step["recipe_id"], step["step_order"], step["step_description"])
        
    async def get_step_descriptions_by_recipe_id(self, recipe_id):
        rows = await self._connection.execute(
            'SELECT * FROM steps WHERE recipe_id = $1', [recipe_id]
            )
        steps = []
        if not rows:
            return None
        else:
            for row in rows:
                step = Step(row["id"], row["recipe_id"], row["step_order"], row["step_description"])
                steps.append(step)
            return steps
        
    async def create_new_step(self, step):
        await self._connection.execute(
            'INSERT INTO steps (recipe_id, step_order, step_description) VALUES ($1, $2, $3)',
            [step.recipe_id, step.step_order, step.step_description])
        return None 
    

    # async def delete_step(self, id):
    #     await self._connection.execute(
    #         'DELETE FROM steps WHERE id = $1', [id]
    #     )
    #     return None
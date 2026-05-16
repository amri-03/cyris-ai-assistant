import os


class SystemStartupValidator:

    def validate_environment(self):

        required_variables = [
            "OPENAI_API_KEY"
        ]

        missing_variables = []

        for variable in required_variables:

            if not os.getenv(variable):
                missing_variables.append(
                    variable
                )

        if missing_variables:
            return {
                "startup_status":
                    "environment_incomplete",

                "missing_variables":
                    missing_variables
            }

        return {
            "startup_status":
                "environment_ready"
        }
class Util:
    @staticmethod
    def isnull(comparion_value):
        null_value = True
        try:
            if comparion_value is not None and comparion_value != "" and comparion_value.lower() != "null"  and comparion_value != "undefined"  and len(comparion_value) > 0:
                null_value = False
        except Exception as e:
            null_value = True
        return null_value
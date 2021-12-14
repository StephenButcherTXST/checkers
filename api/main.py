from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Define default settings for input grid of checkers
grid_config = {
    # Size of the square grid (x = y)
    "size": 8,

    # Number of consecutive checkers to match
    "consecutive_checkers": 4,

    # Expected string values to match black (B), red (R), empty square (-)
    "black": "B", 
    "red": "R", 
    "empty": "-",

    # Require case sensitive matching for black/red/empty values
    "case_sensitive": False,

    # Allow overlapping results
    "allow_overlap": True
}


class ProcessGrid(Resource):
    """ Receive JSON data via POST, and calculate consecutive checkers."""

    def post(self):

        # Read grid data from request. (Note: Service already validates JSON)
        grid = request.get_json(force=True)

        # Check that we have the correct number of rows
        if len(grid) != grid_config["size"]: return { "message": "Invalid grid size" }, 400

        # Empty list to hold results
        results = []

        # Empty list used to prevent overlapping matches (if enabled)
        already_matched_squares = []

        # Consecutive checkers for a match
        match_count = grid_config["consecutive_checkers"]

        # Build string targets by creating a string of "black/red" that is "consecutive_checkers" in length
        black_target = grid_config["black"] * match_count
        red_target = grid_config["red"] * match_count

        # Iterate over grid rows for error checking
        for row in grid:
            # Check that the current row meets grid size requirement
            if len(row) != grid_config["size"]: return { "message": "Invalid grid size" }, 400

        # Re-iterate over grid rows for processing
        row = 0
        while row < len(grid):

            # Check that the current row meets grid size requirement
            if len(grid[row]) != grid_config["size"]: return { "message": "Invalid grid size" }, 400

            # Is exact match (case sensitive) required?
            if grid_config["case_sensitive"] == True:
                # [Case Sensitive] Setup a list of allowed characters
                allowed_chars = [ grid_config["black"], grid_config["red"], grid_config["empty"] ]
            else:
                # [Case Insensitive] Load all the values from the current row into a single string in upper case
                row_str = "".join(grid[row]).upper()
                # Setup a list of allowed characters, force values to upper case
                allowed_chars = [ grid_config["black"].upper(), grid_config["red"].upper(), grid_config["empty"].upper() ]

            # Iterate over columns in current row
            col = 0
            while col < len(grid[row]):

                # Read value in current square
                if grid_config["case_sensitive"] == True: value = grid[row][col] # [Case Sensitive]
                else: value = str(grid[row][col]).upper() # [Case Insensitive]

                # Check that character is allowed
                if value not in allowed_chars: return { "message": f"Invalid character: {grid[row][col]} At position: {col}x{row}" }, 400

                # Setup targets (final x/y location for possible matches)
                match_targets = { 
                        "E": { "x": col + match_count - 1, "y": row },
                        "S": { "x": col, "y": row + match_count - 1 },
                        "SE": { "x": col + match_count - 1, "y": row + match_count - 1 },
                        "SW": { "x": col - match_count + 1, "y": row + match_count - 1 },
                    }

                # Iterate over offsets for each direction
                for direction, target in match_targets.items():
                    # Check that final location is valid within grid
                    if target["x"] < len(grid[row]) and target["x"] >= 0 and target["y"] < len(grid) and target["y"] >= 0:
                        
                        # Process grid for match info
                        match_found, match_color, used_squares = process_squares(grid=grid, start_x=col, start_y=row, end_x=target["x"], 
                            end_y=target["y"], already_matched=already_matched_squares, target_black=black_target, target_red=red_target, case_sensitive=grid_config["case_sensitive"])

                        # Consecutive checkers matched a target color (black/red)
                        if match_found == True:
                            # Append match info to results
                            results.append({"x": col, "y": row, "color": match_color, "direction": direction})
                            # If overlapping is not allowed, add matched locations to list
                            if grid_config["allow_overlap"] == False: already_matched_squares.extend(used_squares)

                # Increment column position
                col += 1

            # Increment row position
            row += 1
        
        # Return result set of matches with color and direction, as list of dictionaries
        # e.g. {"x": 1, "y": 4, "color": "B", "direction": "SE"}
        return results

def process_squares(grid, start_x, start_y, end_x, end_y, already_matched, target_black, target_red, case_sensitive):
    """ 
    Create string from grid, based on start and end positions
    Returns a tuple containing the string and a list of square locations processed to make the string
    """

    # Placeholder for resulting string
    match_string = ""

    # Starting offsets
    x_offset = 0
    y_offset = 0

    # Used for tracking location during while loop
    current_square = (start_y + y_offset, start_x + x_offset)

    # Squares locations processed in this run
    used_squares = []

    # Return values
    match_found = False
    color = None

    while True:
        # Break loop if the current square exists in already_matched
        if current_square in already_matched: break

        # Append next square value to the result string
        match_string += grid[start_y + y_offset][start_x + x_offset]
        
        # Append current square location to used squares list
        used_squares.append(current_square)

        # Increment applicable offsets
        if start_y != end_y: y_offset += 1
        if start_x < end_x: x_offset += 1
        if start_x > end_x: x_offset -= 1

        # Break loop when we reach the end square
        if current_square[0] == end_y and current_square[1] == end_x: break

        # Update current_square to next square location
        current_square = (start_y + y_offset, start_x + x_offset)

    # Do target strings match case sensitive or case insensitive tests? [Black]
    if (case_sensitive == True and target_black == match_string) or \
        (case_sensitive == False and target_black.upper() == match_string.upper()):
        match_found = True
        color = "B" 

    # Do target strings match case sensitive or case insensitive tests? [Red]
    elif (case_sensitive == True and target_red == match_string) or \
        (case_sensitive == False and target_red.upper() == match_string.upper()):
        match_found = True
        color = "R" 

    # Return result string and squares as tuple
    return (match_found, color, used_squares)

api.add_resource(ProcessGrid, '/')

if __name__ == '__main__':
    app.run(debug=True)

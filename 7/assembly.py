import sys
import copy


def find_available(graph, steps):
    return [s for s in steps if s not in graph]


def trim_graph(graph, item):
    removed_keys = []
    for step, items in graph.items():
        if item in items:
            items.remove(item)
            if len(items) == 0:
                removed_keys.append(step)
            else:
                graph[step] = items

    for key in removed_keys:
        del graph[key]
    return graph


def assembly():
    steps = set()
    rules = []
    for directions in sys.stdin:
        parts = directions.split()
        rules.append((parts[1], parts[7]))
        steps.add(parts[1])
        steps.add(parts[7])


    graph = {}
    for requirement, step in rules:
        if step in graph:
            graph[step].append(requirement)
        else:
            graph[step] = [requirement]

    # Iterate through until no steps are remaining
    solution = ""
    current_graph = copy.deepcopy(graph)
    remaining_steps = steps.copy()
    while(current_graph):
        options = find_available(current_graph, remaining_steps)
        choice = min(options)

        #Add to solution and remove from graph and choices
        solution += choice
        remaining_steps.remove(choice)
        current_graph = trim_graph(current_graph, choice)

    # Add final item
    solution += remaining_steps.pop()
    print(f'The correct order is {solution}')

    # Setup variables to simulate progress
    base_seconds = 60
    workers = 5
    total_seconds = 0
    workers = ['free']*workers
    remaining_time = {step: ord(step)-64+base_seconds for step in steps}

    # Process until all steps are completed
    while(steps):
        # Assign workers
        if 'free' in workers:
            options = sorted(find_available(graph, steps))
            for step in options:
                if 'free' in workers and step not in workers:
                    workers[workers.index('free')] = step

        # Decrement time on all active steps
        for step in remaining_time:
            #Only increment steps being worked on
            if step not in workers:
                continue

            remaining_time[step] -= 1

            # If the step is finished, remove it from the graph
            if remaining_time[step] == 0:
                #print(f'Finished {step}')
                steps.remove(step)
                graph = trim_graph(graph, step)
                workers[workers.index(step)] = 'free'

        print(total_seconds,workers,remaining_time)
        total_seconds += 1

    print(f'Assembly took {total_seconds} seconds')


assembly()
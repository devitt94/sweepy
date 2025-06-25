

function SweepstakesList({ sweepstakes, showSweepstakes }) {

    return (
        <div className="mt-6"> 
            <table className="min-w-full border rounded-lg">
                <thead className="bg-gray-100">
                <tr>
                    <th className="px-4 py-2 text-left">ID</th>
                    <th className="px-4 py-2 text-left">Name</th>
                    <th className="px-4 py-2 text-left">No. Participants</th>
                    <th className="px-4 py-2 text-left">Status</th>
                </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                    {sweepstakes.map((p, index) => (
                        <tr key={index} className="cursor-pointer" onClick={() => showSweepstakes(p.id)}>
                            <td className="px-4 py-2">{p.id}</td>
                            <td className="px-4 py-2">{p.name}</td>
                            <td className="px-4 py-2">{p.participants.length}</td>
                            <td className="px-4 py-2">Active</td>
                        </tr>

                    ))}

                </tbody>
            </table>
        </div>  
    );
};

export default SweepstakesList;

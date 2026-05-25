export default function MVPStatusPanel({

                                           mvpState

                                       }) {

    return (

        <div>

            <h3>
                MVP Readiness
            </h3>

            <p>
                {mvpState}
            </p>

        </div>
    );
}